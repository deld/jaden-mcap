// ─────────────────────────────────────────────────────────────────────────
// Spelling sentences - pure helpers, shared by spelling-intake and
// spelling-media, covered by sentences.test.mjs under plain node.
//
// A spelling test is read the teacher's way: the word, a sentence that uses
// it (with the word stressed), then the word again. Imported words used to
// get "Spell the word you hear. ___ (6 letters)" as their "sentence", which
// read aloud as nonsense. Claude now writes a real sentence per word; these
// helpers decide whether what it wrote is fit to read to Jaden.
// ─────────────────────────────────────────────────────────────────────────

/** The old stand-in text - a question still carrying it has no sentence yet. */
export const PLACEHOLDER = /^spell the word you hear\b/i;
export const isPlaceholder = (text) => PLACEHOLDER.test(String(text ?? "").trim());

const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const wholeWord = (word) => new RegExp(`(^|[^A-Za-z'])(${esc(word)})(?=[^A-Za-z']|$)`, "gi");

/** A failure reason for one sentence, or null if it can be read to Jaden. */
export function checkSentence(word, sentence) {
  const w = String(word ?? "").trim().toLowerCase();
  const s = String(sentence ?? "").trim();
  if (!s) return "empty";
  const hits = [...s.matchAll(wholeWord(w))].length;
  if (hits !== 1) return hits ? `uses "${w}" ${hits} times` : `does not use "${w}" exactly`;
  const n = s.split(/\s+/).length;
  if (n < 5) return `too short (${n} words)`;
  if (n > 18) return `too long (${n} words)`;
  if (!/[.!?]["')]?$/.test(s)) return "does not end like a sentence";
  if (/_{2,}/.test(s)) return "contains a blank";
  if (/[<>{}\[\]]/.test(s)) return "contains markup";
  return null;
}

/** "The doctor tested my reflex." -> "The doctor tested my ___." */
export function toCloze(word, sentence) {
  return String(sentence).trim().replace(wholeWord(String(word)), (_, pre) => `${pre}___`);
}

/** What the voice reads: word, sentence, word - with pauses between. */
export function spokenScript(word, sentence) {
  return sentence ? `${word}.\n\n${sentence}\n\n${word}.` : `${word}.`;
}

/** Public storage path for a word's clips: kind is "full" or "word". */
export const audioPath = (word, kind) => `${encodeURIComponent(String(word).toLowerCase())}/${kind}.mp3`;
export const AUDIO_BUCKET = "spelling-audio";

export const SENTENCE_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["sentences"],
  properties: {
    sentences: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["word", "sentence"],
        properties: { word: { type: "string" }, sentence: { type: "string" } },
      },
    },
  },
};

export function sentencePrompt(words) {
  return `You are a 4th-grade teacher in Maryland reading a spelling test aloud. For each spelling word below, write ONE sentence you would say to the class after reading the word, so students hear it used.

Rules for every sentence:
- Use the word EXACTLY as written, once - same form, not plural, not past tense, not another form.
- Make the meaning clear from the sentence, the way a good spelling-test sentence does.
- 8 to 15 words, plain words a 9-year-old knows, one sentence ending in a period.
- Kind, everyday situations: school, home, sports, animals, nature. Nothing scary or upsetting.
- Do not start the sentence with the spelling word, and do not explain its spelling.

Return one entry per word, with "word" copied exactly.

Words:
${words.map((w) => `- ${w}`).join("\n")}`;
}

/**
 * Pair the model's sentences back to the words and keep the good ones.
 * @returns {{ ok: Record<string, string>, bad: { word: string, reason: string }[] }}
 */
export function acceptSentences(words, out) {
  const byWord = new Map((out?.sentences ?? []).map((s) => [String(s.word).trim().toLowerCase(), String(s.sentence).trim()]));
  const ok = {}, bad = [];
  for (const w of words) {
    const s = byWord.get(w.toLowerCase());
    const reason = s == null ? "no sentence returned" : checkSentence(w, s);
    if (reason) bad.push({ word: w, reason }); else ok[w] = s;
  }
  return { ok, bad };
}
