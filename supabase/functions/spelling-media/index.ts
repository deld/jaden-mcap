// ─────────────────────────────────────────────────────────────────────────
// spelling-media - give spelling words a real sentence and recorded audio.
//
// spelling-intake does this for each new list as it arrives. This endpoint
// is for everything else: the words already in the bank, a word whose
// sentence or recording should be redone, or a re-run after OPENAI_API_KEY
// is first set.
//
//   POST ?all=1            every active spelling word missing a sentence or audio
//   POST ?words=a,b        just these words
//        &limit=N          at most N words this call (default 20) - an Edge
//                          Function has a time limit, so a backfill is a few
//                          calls; the reply says how many remain
//        &dry=1            write sentences and return them, change nothing
//        &audio=0          sentences only
//        &force=1          redo sentences and audio even if present
//
// Auth: the shared INTAKE_SECRET, or a service-level key as a Bearer token.
// ─────────────────────────────────────────────────────────────────────────
import { db, enrichSpelling, hasAudio } from "../_shared/spelling-media.ts";
import { isPlaceholder } from "../_shared/sentences.js";

const SHARED_SECRET = Deno.env.get("INTAKE_SECRET") ?? "";
const SERVICE_KEY   = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const SUPABASE_URL  = Deno.env.get("SUPABASE_URL") ?? "";

// A project's service key comes in two forms - the legacy JWT and the newer
// sb_secret_ key - and this function's env holds only one of them. Accept
// either by asking Auth's admin API, which answers only a service-level key.
async function isServiceKey(token: string): Promise<boolean> {
  if (!token) return false;
  if (SERVICE_KEY && token === SERVICE_KEY) return true;
  const r = await fetch(`${SUPABASE_URL}/auth/v1/admin/users?per_page=1`,
    { headers: { apikey: token, Authorization: `Bearer ${token}` } })
    .catch(() => null);
  return !!r?.ok;
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });
  const url = new URL(req.url);
  const given  = req.headers.get("x-intake-secret") ?? url.searchParams.get("secret") ?? "";
  const bearer = (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
  const authed = (SHARED_SECRET && given === SHARED_SECRET) || await isServiceKey(bearer);
  if (!authed) return new Response("unauthorized", { status: 401 });

  const q = url.searchParams;
  const dry = q.get("dry") === "1", force = q.get("force") === "1", audio = q.get("audio") !== "0";
  const limit = Math.max(1, Math.min(60, Number(q.get("limit")) || 20));
  const only = (q.get("words") ?? "").split(",").map((w) => w.trim().toLowerCase()).filter(Boolean);
  if (!only.length && q.get("all") !== "1") {
    return Response.json({ ok: false, error: "pass ?all=1 or ?words=a,b" }, { status: 400 });
  }

  const r = await db(`questions?select=id,correct,text&subject=eq.Spelling&type=eq.spelling&active=eq.true&limit=1000`);
  if (!r.ok) return Response.json({ ok: false, error: `reading questions: HTTP ${r.status}` }, { status: 500 });
  let rows = (await r.json() as { id: string; correct: unknown; text: string }[])
    .filter((x) => typeof x.correct === "string" && x.correct);
  if (only.length) rows = rows.filter((x) => only.includes(String(x.correct).toLowerCase()));

  // What still needs doing: no sentence yet, or (when recording) no audio yet.
  const todo: typeof rows = [];
  for (const x of rows) {
    if (force || isPlaceholder(x.text) || (audio && !(await hasAudio(String(x.correct))))) todo.push(x);
  }
  const words = [...new Set(todo.map((x) => String(x.correct).toLowerCase()))];
  const batch = words.slice(0, limit);
  const batchRows = todo.filter((x) => batch.includes(String(x.correct).toLowerCase()));

  try {
    const report = await enrichSpelling(batchRows, { audio, force, dry });
    return Response.json({ ok: true, dry, words: batch, remaining: words.length - batch.length, ...report });
  } catch (e) {
    return Response.json({ ok: false, error: String((e as Error).message ?? e), words: batch }, { status: 500 });
  }
});
