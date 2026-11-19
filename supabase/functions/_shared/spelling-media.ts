// ─────────────────────────────────────────────────────────────────────────
// Sentences and recorded audio for spelling words.
//
//   writeSentences  Claude writes one teacher-style sentence per word;
//                   sentences.js rejects any that misuse the word.
//   recordClips     OpenAI text-to-speech records two clips per word into
//                   the public spelling-audio bucket:
//                     <word>/full.mp3  word - sentence (word stressed) - word
//                     <word>/word.mp3  the word on its own
//                   Skipped, not failed, until OPENAI_API_KEY is set: the app
//                   falls back to the device voice reading the same script.
//   enrichSpelling  does both for a set of words and saves the sentences.
//
// Used by spelling-intake (new lists) and spelling-media (backfill).
// ─────────────────────────────────────────────────────────────────────────
import Anthropic from "npm:@anthropic-ai/sdk@0.132.1";
import {
  SENTENCE_SCHEMA, sentencePrompt, acceptSentences, toCloze, isPlaceholder,
  spokenScript, audioPath, AUDIO_BUCKET,
} from "./sentences.js";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY  = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const OPENAI_KEY   = Deno.env.get("OPENAI_API_KEY") ?? "";
const TTS_MODEL    = Deno.env.get("OPENAI_TTS_MODEL") ?? "gpt-4o-mini-tts";
const TTS_VOICE    = Deno.env.get("OPENAI_TTS_VOICE") ?? "coral";

const FULL_INSTRUCTIONS =
  "You are a warm, clear 4th-grade teacher giving a spelling test. Speak at a calm, slightly slow pace " +
  "in standard American English. Say the spelling word on its own, pause, read the sentence naturally " +
  "while giving the spelling word clear stress, pause, then say the spelling word once more. " +
  "Pronounce the spelling word carefully and fully every time.";
const WORD_INSTRUCTIONS =
  "Say this single spelling word clearly and slowly, in standard American English, " +
  "the way a teacher says a word in a spelling test.";

export const db = (path: string, init: RequestInit = {}) =>
  fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      ...(init.headers ?? {}),
    },
  });

/** One sentence per word. Words Claude got wrong get one more try on their own. */
export async function writeSentences(words: string[]) {
  const client = new Anthropic();   // ANTHROPIC_API_KEY from the function's secrets
  const ask = async (ws: string[]) => {
    const msg = await client.beta.messages.stream({
      model: "claude-opus-5-5",
      max_tokens: 16000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      output_config: { effort: "low", format: { type: "json_schema", schema: SENTENCE_SCHEMA } },
      messages: [{ role: "user", content: sentencePrompt(ws) }],
    }).finalMessage();
    if (msg.stop_reason === "refusal") throw new Error("The model declined to write sentences");
    if (msg.stop_reason === "max_tokens") throw new Error("The model ran out of room");
    return JSON.parse(msg.content.flatMap((b) => (b.type === "text" ? [b.text] : [])).join(""));
  };
  const first = acceptSentences(words, await ask(words));
  if (!first.bad.length) return first;
  const retry = acceptSentences(first.bad.map((b) => b.word), await ask(first.bad.map((b) => b.word)));
  return { ok: { ...first.ok, ...retry.ok }, bad: retry.bad };
}

const publicUrl = (word: string, kind: string) =>
  `${SUPABASE_URL}/storage/v1/object/public/${AUDIO_BUCKET}/${audioPath(word, kind)}`;

export async function hasAudio(word: string): Promise<boolean> {
  const r = await fetch(publicUrl(word, "full"), { method: "HEAD" }).catch(() => null);
  return !!r?.ok;
}

async function speak(input: string, instructions: string): Promise<ArrayBuffer> {
  const r = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: { Authorization: `Bearer ${OPENAI_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: TTS_MODEL, voice: TTS_VOICE, input, instructions, response_format: "mp3" }),
  });
  if (!r.ok) throw new Error(`OpenAI speech: HTTP ${r.status} ${(await r.text()).slice(0, 200)}`);
  return await r.arrayBuffer();
}

async function store(word: string, kind: string, mp3: ArrayBuffer) {
  const r = await fetch(`${SUPABASE_URL}/storage/v1/object/${AUDIO_BUCKET}/${audioPath(word, kind)}`, {
    method: "POST",
    headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${SERVICE_KEY}`,
               "Content-Type": "audio/mpeg", "x-upsert": "true", "Cache-Control": "max-age=3600" },
    body: mp3,
  });
  if (!r.ok) throw new Error(`storing ${word}/${kind}: HTTP ${r.status} ${await r.text()}`);
}

/** Record both clips for a word. Returns false when no OpenAI key is set. */
export async function recordClips(word: string, sentence: string): Promise<boolean> {
  if (!OPENAI_KEY) return false;
  await store(word, "word", await speak(word, WORD_INSTRUCTIONS));
  await store(word, "full", await speak(spokenScript(word, sentence), FULL_INSTRUCTIONS));
  return true;
}

type Row = { id: string; correct: unknown; text: string };
const sentenceOf = (r: Row) => isPlaceholder(r.text) ? "" :
  String(r.text).replace(/\s*\(\d+ letters\)\s*$/, "").replace(/_{2,}/, String(r.correct));

/**
 * Give these spelling questions a sentence (where they still have the
 * stand-in text) and recorded audio (where it is missing or `force`).
 */
export async function enrichSpelling(rows: Row[], { audio = true, force = false, dry = false } = {}) {
  const report = { sentences: 0, audio: 0, audioSkipped: false, bad: [] as { word: string; reason: string }[],
                   written: {} as Record<string, string> };
  const needSentence = rows.filter((r) => force || isPlaceholder(r.text));
  const words = [...new Set(needSentence.map((r) => String(r.correct).toLowerCase()))];
  const sentences: Record<string, string> = {};
  if (words.length) {
    const { ok, bad } = await writeSentences(words);
    Object.assign(sentences, ok);
    report.bad.push(...bad);
    report.written = ok;
  }
  if (dry) return report;

  for (const r of needSentence) {
    const w = String(r.correct).toLowerCase();
    if (!sentences[w]) continue;
    const u = await db(`questions?id=eq.${r.id}`, {
      method: "PATCH", body: JSON.stringify({ text: toCloze(w, sentences[w]) }),
    });
    if (u.ok) { report.sentences++; r.text = toCloze(w, sentences[w]); }
    else report.bad.push({ word: w, reason: `saving the sentence failed: HTTP ${u.status}` });
  }

  if (!audio) return report;
  if (!OPENAI_KEY) { report.audioSkipped = true; return report; }
  for (const r of rows) {
    const w = String(r.correct).toLowerCase();
    if (!force && await hasAudio(w)) continue;
    try { if (await recordClips(w, sentenceOf(r))) report.audio++; }
    catch (e) { report.bad.push({ word: w, reason: String((e as Error).message ?? e) }); }
  }
  return report;
}
