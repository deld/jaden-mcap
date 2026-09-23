// ─────────────────────────────────────────────────────────────────────────
// spelling-intake — webhook for the weekly spelling list.
//
//   Teacher emails ClassroomParent  ->  Gmail filter forwards to CloudMailin
//   ->  CloudMailin POSTs JSON here  ->  we read the linked Google Doc,
//   find Jaden's group on the roster, take that group's words, and publish
//   them as typed-spelling questions.
//
// This endpoint is PUBLIC (verify_jwt is off, because CloudMailin cannot send
// a Supabase JWT), so it authenticates with a shared secret. Without that, any
// stranger could POST questions into a child's homework app.
//
// It publishes on success and records every run either way. It refuses to
// publish anything it is not confident about: the doc's shape is the
// teacher's to change, and a wrong list reaching Jaden is worse than an
// import that visibly failed.
// ─────────────────────────────────────────────────────────────────────────
import { parseSpellingDoc, findDocCandidates, docExportUrl } from "./parse.js";

const SUPABASE_URL  = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY   = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SHARED_SECRET = Deno.env.get("INTAKE_SECRET") ?? "";
const STUDENT = "Jaden";
const GRADE = 4;

const db = (path: string, init: RequestInit = {}) =>
  fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      ...(init.headers ?? {}),
    },
  });

/** Monday of the week containing `d`, as YYYY-MM-DD. */
function weekOf(d = new Date()): string {
  const x = new Date(d);
  x.setHours(0, 0, 0, 0);
  x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
  return x.toISOString().slice(0, 10);
}

function prefixHint(word: string): string {
  for (const [p, meaning] of [
    ["micro", "small"], ["mega", "great or large"], ["super", "above or beyond"],
    ["hyper", "over or excessive"], ["trans", "across"], ["inter", "between"],
    ["sub", "under"], ["pre", "before"], ["re", "again"],
  ] as const) {
    if (word.startsWith(p) && word.length > p.length + 2) {
      return `${p}- means "${meaning}". Say the parts: ${p}- + ${word.slice(p.length)}.`;
    }
  }
  return `Say it slowly and write the sounds you hear: ${word}`;
}

/** A cloze sentence is better than nothing, but we do not invent a false context. */
const clozeFor = (w: string) => `Spell the word you hear. ___ (${w.length} letters)`;

async function recordRun(row: Record<string, unknown>) {
  await db("intake_runs", { method: "POST", body: JSON.stringify(row) }).catch(() => {});
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  // ── Shared-secret auth ────────────────────────────────────────────────
  const url = new URL(req.url);
  const given = req.headers.get("x-intake-secret") ?? url.searchParams.get("secret") ?? "";
  // ?dry=1 parses and reports without writing anything - use it to confirm a
  // real doc reads correctly before letting the first live email publish.
  const dryRun = url.searchParams.get("dry") === "1";
  if (!SHARED_SECRET || given !== SHARED_SECRET) {
    return new Response("unauthorized", { status: 401 });
  }

  let subject = "", body = "", from = "";
  try {
    const p = await req.json();
    // CloudMailin's JSON shape; tolerate the common variants.
    subject = p?.headers?.subject ?? p?.envelope?.subject ?? p?.subject ?? "";
    from    = p?.headers?.from ?? p?.envelope?.from ?? p?.from ?? "";
    body    = [p?.html, p?.plain, p?.text, p?.body].filter(Boolean).join("\n");
  } catch {
    return new Response("bad json", { status: 400 });
  }

  const base = { student: STUDENT, subject_line: subject, sender: from };

  // Only act on spelling mail; anything else is acknowledged and ignored so
  // a broad Gmail filter cannot cause junk imports.
  if (!/spelling/i.test(subject)) {
    await recordRun({ ...base, status: "ignored", detail: "subject is not a spelling list" });
    return Response.json({ ok: true, action: "ignored" });
  }

  try {
    // Real ClassroomParent mail has no direct Docs URL - the list is behind a
    // click-tracker, so candidates are followed until one lands on a Doc.
    // findDocCandidates has already excluded anything resembling unsubscribe.
    const candidates = findDocCandidates(body).slice(0, 4);
    let docUrl = "", html = "";
    const tried: string[] = [];
    for (const c of candidates) {
      const direct = docExportUrl(c);
      const target = direct ?? c;
      let res: Response;
      try {
        res = await fetch(target, { redirect: "follow", headers: { "User-Agent": "Mozilla/5.0" } });
      } catch (err) {
        tried.push(`${c} -> ${String(err)}`);
        continue;
      }
      const landed = docExportUrl(res.url) ?? direct;
      if (!landed) { tried.push(`${c} -> ${res.url}`); continue; }
      // A tracker resolves to /edit; fetch the export of wherever it landed.
      const exp = await fetch(landed, { redirect: "follow" });
      if (!exp.ok) {
        throw new Error(`Found the doc but could not read it (HTTP ${exp.status}). Is it shared "anyone with the link"?`);
      }
      docUrl = landed;
      html = await exp.text();
      break;
    }
    if (!html) {
      throw new Error(`No Google Doc behind any link in this email. Tried: ${tried.join(" | ") || "nothing"}`);
    }

    const { group, words, columnHeader } = parseSpellingDoc(html, STUDENT);
    const week = weekOf();

    if (dryRun) {
      return Response.json({ ok: true, action: "dry-run", week, group, columnHeader,
                             words, count: words.length, note: "nothing was written" });
    }

    // Idempotency: a re-forwarded email must not double-publish.
    const dupe = await db(
      `questions?select=id&subject=eq.Spelling&type=eq.spelling&assignment=eq.${encodeURIComponent(`Spelling week of ${week}`)}&limit=1`,
    ).then((r) => r.json());
    if (Array.isArray(dupe) && dupe.length) {
      await recordRun({ ...base, status: "duplicate", week_of: week, group_name: group, word_count: words.length,
                        detail: "a list for this week is already published" });
      return Response.json({ ok: true, action: "duplicate", week, words: words.length });
    }

    const packet = await db("packets", {
      method: "POST",
      headers: { Prefer: "return=representation" },
      body: JSON.stringify({
        student: STUDENT, grade: GRADE, subject: "Spelling", week_of: week, status: "approved",
        notes: `Auto-imported from ${from || "the weekly spelling email"} on ${new Date().toISOString().slice(0, 10)}. `
             + `Group "${group}" (column "${columnHeader}"), ${words.length} words. Source: ${docUrl}`,
      }),
    }).then((r) => r.json());

    const rows = words.map((w) => ({
      grade: GRADE, subject: "Spelling", domain: "Words Their Way", category: group,
      type: "spelling", text: clozeFor(w), options: null, correct: w,
      hint: prefixHint(w),
      solution: `Listen to the word, say each part, then write it: ${w}`,
      active: true, source: "packet", track: "test_prep",
      assignment: `Spelling week of ${week}`,
    }));
    const ins = await db("questions", {
      method: "POST", headers: { Prefer: "return=minimal" }, body: JSON.stringify(rows),
    });
    if (!ins.ok) throw new Error(`Insert failed: HTTP ${ins.status} ${await ins.text()}`);

    await recordRun({ ...base, status: "published", week_of: week, group_name: group,
                      word_count: words.length, doc_url: docUrl,
                      packet_id: Array.isArray(packet) ? packet[0]?.id : null,
                      detail: words.join(", ") });

    return Response.json({ ok: true, action: "published", week, group, words: words.length });
  } catch (e) {
    // Refused, not crashed: nothing was published and the reason is recorded.
    const msg = String((e as Error).message ?? e);
    if (dryRun) return Response.json({ ok: false, action: "dry-run-failed", error: msg });
    await recordRun({ ...base, status: "failed", detail: msg });
    return Response.json({ ok: false, action: "failed", error: msg }, { status: 200 });
  }
});
