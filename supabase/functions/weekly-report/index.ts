// ─────────────────────────────────────────────────────────────────────────
// weekly-report - emails each linked parent a summary of their student's
// practice for the week that just ended.
//
//   pg_cron (Monday 7am Eastern)  ->  POST here with REPORT_SECRET
//   ->  for every student with parents linked in `parents`
//   ->  summarise last Mon-Sun from attempts / question_attempts
//   ->  one email per parent, sent through Gmail SMTP
//   ->  record the run in report_runs (so a second firing does not resend)
//
// There is no domain to send from, so mail goes out through a Gmail account
// with an app password. Gmail signs it, so it lands in the inbox rather than
// spam - which a third-party sender claiming a gmail.com From would not.
// ─────────────────────────────────────────────────────────────────────────
import nodemailer from "npm:nodemailer@7.0.13";
import { lastFullWeek, summarize, renderEmail, TZ } from "./report.js";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_KEY  = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SECRET       = Deno.env.get("REPORT_SECRET") ?? "";
const GMAIL_USER   = Deno.env.get("GMAIL_USER") ?? "";
const GMAIL_PASS   = Deno.env.get("GMAIL_APP_PASSWORD") ?? "";
const APP_URL      = Deno.env.get("APP_URL") ?? ""; // the app's address, for an "Open the app" link

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

async function rows(path: string): Promise<any[]> {
  const r = await db(path);
  if (!r.ok) throw new Error(`${path.split("?")[0]}: HTTP ${r.status} ${await r.text()}`);
  return r.json();
}

type Parent = { name: string | null; email: string; student: string };

async function buildFor(student: string, week: ReturnType<typeof lastFullWeek>) {
  const s = encodeURIComponent(student);
  const from = new Date(week.start.getTime() - 7 * 864e5).toISOString(); // prior week too, for trends
  const to = week.end.toISOString();
  const [attempts, qa, imports] = await Promise.all([
    rows(`attempts?student=eq.${s}&created_at=gte.${week.start.toISOString()}&created_at=lt.${to}` +
         `&select=created_at,total,score,time_sec,completed,abandoned,subject&limit=2000`),
    rows(`question_attempts?student=eq.${s}&created_at=gte.${from}&created_at=lt.${to}` +
         `&select=created_at,subject,domain,category,correct,question_text,your_answer,correct_answer&limit=10000`),
    rows(`intake_runs?student=eq.${s}&status=eq.published&created_at=gte.${week.start.toISOString()}&created_at=lt.${to}&select=*`)
      .catch(() => []), // an older intake_runs schema must not cost the whole report
  ]);
  return summarize({ attempts, qa, imports, week, tz: TZ });
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });
  const url = new URL(req.url);
  const given = req.headers.get("x-report-secret") ?? url.searchParams.get("secret") ?? "";
  if (!SECRET || given !== SECRET) return new Response("unauthorized", { status: 401 });

  // ?dry=1    render and return the emails, send nothing
  // ?to=addr  send only to that parent (must be linked) - for a first test
  // ?force=1  send even if this week's report already went out
  const dryRun = url.searchParams.get("dry") === "1";
  const onlyTo = (url.searchParams.get("to") ?? "").toLowerCase();
  const force = url.searchParams.get("force") === "1";
  const week = lastFullWeek(url.searchParams.get("now") ? new Date(url.searchParams.get("now")!) : new Date(), TZ);

  let parents: Parent[];
  try {
    parents = await rows("parents?receives_report=eq.true&select=name,email,student&order=student");
  } catch (e) {
    return Response.json({ ok: false, error: String((e as Error).message ?? e) }, { status: 500 });
  }
  if (onlyTo) parents = parents.filter((p) => p.email.toLowerCase() === onlyTo);
  if (!parents.length) {
    return Response.json({ ok: false, error: onlyTo ? `${onlyTo} is not a linked parent` : "no parents linked" });
  }

  if (!dryRun && (!GMAIL_USER || !GMAIL_PASS)) {
    return Response.json({ ok: false, error: "GMAIL_USER / GMAIL_APP_PASSWORD are not set" }, { status: 500 });
  }
  // Port 465 (implicit TLS): Supabase Edge Functions block outbound 25 and 587.
  const mailer = dryRun ? null : nodemailer.createTransport({
    host: "smtp.gmail.com", port: 465, secure: true, auth: { user: GMAIL_USER, pass: GMAIL_PASS },
  });

  const byStudent = new Map<string, Parent[]>();
  for (const p of parents) byStudent.set(p.student, [...(byStudent.get(p.student) ?? []), p]);

  const results: unknown[] = [];
  for (const [student, list] of byStudent) {
    if (!dryRun && !force && !onlyTo) {
      const sent = await rows(`report_runs?student=eq.${encodeURIComponent(student)}&week_of=eq.${week.weekOf}&status=eq.sent&limit=1`)
        .catch(() => []);
      if (sent.length) { results.push({ student, action: "already-sent", week: week.weekOf }); continue; }
    }
    try {
      const summary = await buildFor(student, week);
      const emails = list.map((p) => ({ to: p.email, ...renderEmail(summary, { student, parentName: p.name, appUrl: APP_URL }) }));
      if (dryRun) { results.push({ student, action: "dry-run", week: week.weekOf, summary, emails }); continue; }

      const failures: string[] = [];
      for (const e of emails) {
        try {
          await mailer!.sendMail({ from: `"${student}'s practice" <${GMAIL_USER}>`, to: e.to,
                                   subject: e.subject, text: e.text, html: e.html });
        } catch (err) { failures.push(`${e.to}: ${String((err as Error).message ?? err)}`); }
      }
      const status = failures.length === emails.length ? "failed" : "sent";
      await db("report_runs", { method: "POST", body: JSON.stringify({
        student, week_of: week.weekOf, status, recipients: emails.length - failures.length,
        detail: failures.length ? failures.join("; ") : `${summary.sessions} sessions, ${summary.questions} questions`,
      }) }).catch(() => {});
      results.push({ student, action: status, week: week.weekOf, sent: emails.length - failures.length, failures });
    } catch (e) {
      const msg = String((e as Error).message ?? e);
      if (!dryRun) {
        await db("report_runs", { method: "POST", body: JSON.stringify({
          student, week_of: week.weekOf, status: "failed", recipients: 0, detail: msg }) }).catch(() => {});
      }
      results.push({ student, action: "failed", error: msg });
    }
  }
  return Response.json({ ok: true, week: week.weekOf, results });
});
