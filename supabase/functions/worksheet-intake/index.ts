// ─────────────────────────────────────────────────────────────────────────
// worksheet-intake - webhook for worksheets sent in by email.
//
//   Parent emails photos or a PDF of a worksheet to a CloudMailin address
//   ->  CloudMailin POSTs JSON (attachments included) here
//   ->  Claude reads the pages and writes NEW practice on the same skills
//   ->  a second, blind Claude pass solves every question; disagreements
//       are dropped
//   ->  survivors are inserted INACTIVE, and the app asks a parent to
//       Publish or Discard them.
//
// Same posture as spelling-intake: PUBLIC endpoint (CloudMailin cannot send a
// Supabase JWT), shared-secret auth, sender allow-list, every run recorded.
// The app's Upload button reaches the same pipeline with a parent's sign-in
// token instead of the secret.
// Unlike spelling, the output is model-written, so it never goes live on its
// own: a person looks at it first.
// ─────────────────────────────────────────────────────────────────────────
import Anthropic from "npm:@anthropic-ai/sdk@0.132.1";
import {
  triage, pickAttachments, checkWorksheet, reconcile, solverView, toRows, assignmentName,
  GENERATE_SCHEMA, GENERATE_PROMPT, SOLVE_SCHEMA, SOLVE_PROMPT, MIN_QUESTIONS, MAX_QUESTIONS,
} from "./worksheet.js";

declare const EdgeRuntime: { waitUntil(p: Promise<unknown>): void } | undefined;

const SUPABASE_URL  = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY   = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SHARED_SECRET = Deno.env.get("INTAKE_SECRET") ?? "";
const ALLOWED_FROM = (Deno.env.get("INTAKE_ALLOWED_FROM") ??
  "lt.dzirasa@gmail.com,delali.dzirasa@gmail.com")
  .split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);
const MODEL = "claude-opus-5-5";
const STUDENT = "Jaden";
const GRADE = 4;

const anthropic = new Anthropic(); // ANTHROPIC_API_KEY from the function's secrets

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

async function startRun(row: Record<string, unknown>): Promise<string | null> {
  const r = await db("intake_runs", {
    method: "POST", headers: { Prefer: "return=representation" },
    body: JSON.stringify({ kind: "worksheet", student: STUDENT, ...row }),
  }).catch(() => null);
  if (!r?.ok) return null;
  return (await r.json())[0]?.id ?? null;
}

async function finishRun(id: string | null, row: Record<string, unknown>) {
  if (!id) { await startRun(row); return; }
  await db(`intake_runs?id=eq.${id}`, { method: "PATCH", body: JSON.stringify(row) }).catch(() => {});
}

function toBase64(buf: ArrayBuffer): string {
  const bytes = new Uint8Array(buf);
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

async function sha256(parts: string[]): Promise<string> {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(parts.join("|")));
  return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

/** One structured-output call. Throws on a refusal or a truncated answer. */
async function ask(content: Anthropic.Beta.BetaContentBlockParam[], schema: Record<string, unknown>) {
  const msg = await anthropic.beta.messages.stream({
    model: MODEL,
    max_tokens: 32000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    output_config: { effort: "medium", format: { type: "json_schema", schema } },
    messages: [{ role: "user", content }],
  }).finalMessage();
  if (msg.stop_reason === "refusal") throw new Error("The model declined to process this worksheet");
  if (msg.stop_reason === "max_tokens") throw new Error("The model ran out of room before finishing");
  const text = msg.content.flatMap((b) => (b.type === "text" ? [b.text] : [])).join("");
  return JSON.parse(text);
}

type Page = { name: string; mediaType: string; data?: string; url?: string };

async function readWorksheet(pages: Page[], note: string) {
  const blocks: Anthropic.Beta.BetaContentBlockParam[] = pages.map((p) =>
    p.mediaType === "application/pdf"
      ? { type: "document", source: { type: "base64", media_type: "application/pdf", data: p.data! } }
      : { type: "image", source: { type: "base64", media_type: p.mediaType as "image/jpeg", data: p.data! } });
  const prompt = note ? `${GENERATE_PROMPT}\n\nThe parent who sent it wrote:\n${note}` : GENERATE_PROMPT;

  const out = await ask([...blocks, { type: "text", text: prompt }], GENERATE_SCHEMA);
  checkWorksheet(out);
  const written = out.questions.slice(0, MAX_QUESTIONS);

  const solved = await ask([{ type: "text", text: `${SOLVE_PROMPT}\n\n${solverView(written)}` }], SOLVE_SCHEMA);
  const { kept, dropped } = reconcile(written, solved.answers);
  if (kept.length < MIN_QUESTIONS) {
    throw new Error(`Only ${kept.length} of ${written.length} questions passed checking (need ${MIN_QUESTIONS}). ` +
      `Dropped: ${dropped.slice(0, 4).map((d) => d.reason).join("; ")}`);
  }
  return { out, written, kept, dropped };
}

/** Email addresses in `parents`. Any linked parent may send a worksheet. */
async function parentEmails(): Promise<string[]> {
  const rows = await db("parents?select=email&limit=500").then((r) => (r.ok ? r.json() : [])).catch(() => []);
  return (Array.isArray(rows) ? rows : []).map((r: { email: string }) => String(r.email).trim().toLowerCase());
}

/**
 * The signed-in parent behind a Supabase Auth access token, or null. The
 * token proves an email address; the `parents` table decides whether that
 * address may upload. The app's anon key is also a JWT, but it has no user,
 * so it fails here.
 */
async function uploaderFrom(token: string): Promise<string | null> {
  if (!token) return null;
  const r = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { apikey: SERVICE_KEY, Authorization: `Bearer ${token}` },
  }).catch(() => null);
  if (!r?.ok) return null;
  const email = String((await r.json())?.email ?? "").toLowerCase();
  return email && (await parentEmails()).includes(email) ? email : null;
}

// The in-app upload calls this from the browser, so it must answer CORS.
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-intake-secret",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  const res = await handle(req);
  for (const [k, v] of Object.entries(CORS)) res.headers.set(k, v);
  return res;
});

async function handle(req: Request): Promise<Response> {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  // Two ways in. CloudMailin relays email with the shared secret; the app's
  // upload button sends a parent's sign-in token instead. Either way the
  // sender must be a known parent.
  const url = new URL(req.url);
  const given = req.headers.get("x-intake-secret") ?? url.searchParams.get("secret") ?? "";
  // ?dry=1 reads the worksheet and returns the questions without writing
  // anything, so a real worksheet can be tried before the first live email.
  const dryRun = url.searchParams.get("dry") === "1";
  const viaEmail = Boolean(SHARED_SECRET) && given === SHARED_SECRET;
  const uploader = viaEmail ? null
    : await uploaderFrom((req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, ""));
  if (!viaEmail && !uploader) {
    return Response.json({ ok: false, error: "Sign in as a linked parent to upload." }, { status: 401 });
  }

  let payload: Record<string, any>;
  try { payload = await req.json(); } catch { return new Response("bad json", { status: 400 }); }
  const subject = payload?.headers?.subject ?? payload?.envelope?.subject ?? payload?.subject ?? "";
  const from    = uploader ?? payload?.headers?.from ?? payload?.envelope?.from ?? payload?.from ?? "";
  // What the parent typed ("fractions, pages 46-53") helps; a quoted thread does not.
  const note = [subject, String(payload?.plain ?? "").split(/\n-- ?\n|\nOn .+wrote:/)[0]]
    .map((s) => String(s).trim()).filter(Boolean).join("\n").slice(0, 1000);
  const base = { subject_line: uploader ? `Uploaded in the app${subject ? `: ${subject}` : ""}` : subject, sender: from };

  if (viaEmail) {
    const gate = triage({ from, allowedFrom: [...ALLOWED_FROM, ...(await parentEmails())] });
    if (!gate.process) {
      if (!dryRun) await startRun({ ...base, status: "ignored", detail: gate.detail });
      return Response.json({ ok: true, action: "ignored", reason: gate.detail });
    }
  }

  let pages: Page[];
  try {
    pages = pickAttachments(payload);
    for (const p of pages) {
      if (p.data) continue;
      const r = await fetch(p.url!);
      if (!r.ok) throw new Error(`Could not download ${p.name} (HTTP ${r.status})`);
      p.data = toBase64(await r.arrayBuffer());
    }
  } catch (e) {
    const msg = String((e as Error).message ?? e);
    if (!dryRun) await startRun({ ...base, status: "failed", detail: msg });
    return Response.json({ ok: false, action: "failed", error: msg });
  }

  if (dryRun) {
    try {
      const { out, kept, dropped } = await readWorksheet(pages, note);
      return Response.json({ ok: true, action: "dry-run", subject: out.subject, domain: out.domain,
                             title: out.title, skills: out.skills, kept, dropped, note: "nothing was written" });
    } catch (e) {
      return Response.json({ ok: false, action: "dry-run-failed", error: String((e as Error).message ?? e) });
    }
  }

  // The same pages sent twice (or a CloudMailin retry) must not make a second set.
  // A run cut off mid-way stays "processing"; past 15 minutes it no longer
  // blocks a resend, matching when the app starts calling it failed.
  const hash = await sha256(pages.map((p) => p.data!));
  const cutoff = new Date(Date.now() - 15 * 60e3).toISOString();
  const seen = await db(
    `intake_runs?select=id,status&kind=eq.worksheet&source_hash=eq.${hash}` +
    `&or=(status.in.(review,published),and(status.eq.processing,created_at.gte.${cutoff}))&limit=1`,
  ).then((r) => (r.ok ? r.json() : [])).catch(() => []);
  if (Array.isArray(seen) && seen.length) {
    await startRun({ ...base, status: "duplicate", source_hash: hash, detail: `same pages as an earlier run (${seen[0].status})` });
    return Response.json({ ok: true, action: "duplicate" });
  }

  const runId = await startRun({ ...base, status: "processing", source_hash: hash,
                                 detail: `${pages.length} attachment(s): ${pages.map((p) => p.name).join(", ")}` });

  // Reading and checking takes longer than CloudMailin waits for a reply, so
  // answer now and finish in the background. The run row carries the outcome.
  const work = (async () => {
    try {
      const { out, written, kept, dropped } = await readWorksheet(pages, note);

      const taken = await db(
        `questions?select=assignment&grade=eq.${GRADE}&track=eq.classwork&assignment=not.is.null&limit=5000`,
      ).then((r) => (r.ok ? r.json() : [])).catch(() => []);
      const assignment = assignmentName(out.title, new Date(),
        (Array.isArray(taken) ? taken : []).map((r: { assignment: string }) => r.assignment));

      const packet = await db("packets", {
        method: "POST", headers: { Prefer: "return=representation" },
        body: JSON.stringify({
          student: STUDENT, grade: GRADE, subject: out.subject, status: "processed",
          week_of: new Date().toISOString().slice(0, 10),
          notes: `Emailed in by ${from || "unknown"}. ${out.skills} ` +
                 `${kept.length} of ${written.length} generated questions agreed with an independent solve.`,
        }),
      }).then((r) => r.json()).catch(() => null);

      const ins = await db("questions?select=id", {
        method: "POST", headers: { Prefer: "return=representation" },
        body: JSON.stringify(toRows(kept, { subject: out.subject, domain: out.domain, assignment, grade: GRADE })),
      });
      if (!ins.ok) throw new Error(`Insert failed: HTTP ${ins.status} ${await ins.text()}`);
      const ids = (await ins.json()).map((r: { id: string }) => r.id);

      await finishRun(runId, {
        status: "review", assignment, subject: out.subject, question_count: ids.length, question_ids: ids,
        packet_id: Array.isArray(packet) ? packet[0]?.id : null,
        detail: out.skills + (dropped.length ? ` (${dropped.length} dropped: ${dropped.map((d) => d.reason).join("; ")})` : ""),
      });
    } catch (e) {
      // Refused, not crashed: nothing was inserted and the reason is recorded.
      await finishRun(runId, { status: "failed", detail: String((e as Error).message ?? e) });
    }
  })();

  if (typeof EdgeRuntime !== "undefined") EdgeRuntime.waitUntil(work);
  else await work;
  return Response.json({ ok: true, action: "processing", run: runId, pages: pages.length });
}
