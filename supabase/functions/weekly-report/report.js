// ─────────────────────────────────────────────────────────────────────────
// The weekly progress email: what a week of practice adds up to, and the
// email that says so. Pure - no network - so report.test.mjs covers it.
//
// The numbers follow the app's own Progress screen, so a parent who opens
// the app sees the same figures: a session counts if it ENDED (by the clock
// or by walking away) with at least one answer, and topic accuracy comes
// from per-question rows, not session totals.
// ─────────────────────────────────────────────────────────────────────────

export const TZ = "America/New_York";

const DOMAIN_LABELS = {
  Math: { OA: "Operations & Algebraic Thinking", NBT: "Number & Operations in Base Ten",
          NF: "Fractions", MD: "Measurement & Data", G: "Geometry" },
  Reading: { RL: "Literary Text", RI: "Informational Text", L: "Language" },
  Spelling: {},
};
const SUBJECTS = ["Math", "Reading", "Spelling"];

// ── Dates in the family's time zone ──────────────────────────────────────
function localParts(d, tz) {
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", {
    timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", weekday: "short", hourCycle: "h23",
  }).formatToParts(d).map((x) => [x.type, x.value]));
  return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour, min: +p.minute, s: +p.second, wd: p.weekday };
}

/** The UTC instant of local midnight on y-m-d in `tz`, DST included. */
export function zonedMidnight(y, m, d, tz = TZ) {
  let t = Date.UTC(y, m - 1, d);
  for (let i = 0; i < 2; i++) {
    const p = localParts(new Date(t), tz);
    const asUtc = Date.UTC(p.y, p.m - 1, p.d, p.h, p.min, p.s);
    t -= asUtc - Date.UTC(y, m - 1, d);
  }
  return new Date(t);
}

/** "2026-10-12" for the local calendar day of `d`. */
export function localDay(d, tz = TZ) {
  const p = localParts(new Date(d), tz);
  return `${p.y}-${String(p.m).padStart(2, "0")}-${String(p.d).padStart(2, "0")}`;
}

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

/**
 * The most recent COMPLETE Monday-to-Sunday week before `now`, in `tz`.
 * Sent on a Monday morning, that is the week that just ended.
 */
export function lastFullWeek(now = new Date(), tz = TZ) {
  const p = localParts(now, tz);
  const back = WEEKDAYS.indexOf(p.wd) + 7;           // days back to last week's Monday
  const mon = new Date(Date.UTC(p.y, p.m - 1, p.d - back));
  const nextMon = new Date(Date.UTC(p.y, p.m - 1, p.d - back + 7));
  const start = zonedMidnight(mon.getUTCFullYear(), mon.getUTCMonth() + 1, mon.getUTCDate(), tz);
  const end = zonedMidnight(nextMon.getUTCFullYear(), nextMon.getUTCMonth() + 1, nextMon.getUTCDate(), tz);
  const days = Array.from({ length: 7 }, (_, i) => {
    const x = new Date(Date.UTC(p.y, p.m - 1, p.d - back + i));
    return x.toISOString().slice(0, 10);
  });
  return { start, end, days, weekOf: days[0] };
}

// ── Summarising ──────────────────────────────────────────────────────────
const inRange = (ts, a, b) => { const t = new Date(ts).getTime(); return t >= a.getTime() && t < b.getTime(); };
const pct = (c, n) => (n ? Math.round((c / n) * 100) : null);
const LETTERS_ONLY = /^[A-H](,[A-H])*$/;

function tally(rows, keyOf) {
  const out = {};
  for (const r of rows) {
    const k = keyOf(r);
    if (!k) continue;
    const b = out[k] || (out[k] = { n: 0, c: 0 });
    b.n++; if (r.correct) b.c++;
  }
  return out;
}

/**
 * attempts: session rows; qa: question_attempts rows (this week AND the week
 * before - split here by date); imports: intake_runs rows.
 * @param {{ attempts?: any[], qa?: any[], imports?: any[],
 *           week: { start: Date, end: Date, days: string[], weekOf: string }, tz?: string }} args
 */
export function summarize({ attempts = [], qa = [], imports = [], week, tz = TZ }) {
  const prevStart = new Date(week.start.getTime() - 7 * 864e5);
  const sessions = attempts.filter((a) =>
    (a.completed || a.abandoned) && (a.total || 0) > 0 && inRange(a.created_at, week.start, week.end));
  const thisQa = qa.filter((r) => inRange(r.created_at, week.start, week.end));
  const prevQa = qa.filter((r) => inRange(r.created_at, prevStart, week.start));

  const minutesByDay = Object.fromEntries(week.days.map((d) => [d, 0]));
  const sessionsByDay = Object.fromEntries(week.days.map((d) => [d, 0]));
  for (const s of sessions) {
    const d = localDay(s.created_at, tz);
    if (d in minutesByDay) { minutesByDay[d] += (s.time_sec || 0) / 60; sessionsByDay[d]++; }
  }

  const questions = sessions.reduce((n, s) => n + (s.total || 0), 0);
  const correct = sessions.reduce((n, s) => n + (s.score || 0), 0);

  const cur = tally(thisQa, (r) => r.subject);
  const prev = tally(prevQa, (r) => r.subject);
  const subjects = SUBJECTS.filter((s) => cur[s]).map((s) => ({
    subject: s, n: cur[s].n, pct: pct(cur[s].c, cur[s].n),
    prevPct: prev[s] ? pct(prev[s].c, prev[s].n) : null,
  }));

  // Topics: the sheet's own category name when there is one, else the domain.
  // Spelling's category is the reading GROUP ("Sky"), which says nothing to a
  // parent as a topic.
  const topicName = (r) => r.subject === "Spelling" ? "Weekly words"
    : r.category || (DOMAIN_LABELS[r.subject] || {})[r.domain] || r.domain;
  const topics = Object.entries(tally(thisQa, (r) => (topicName(r) ? `${r.subject}|${topicName(r)}` : null)))
    .map(([k, b]) => ({ subject: k.split("|")[0], topic: k.split("|")[1], n: b.n, pct: pct(b.c, b.n) }));
  // Too few tries says nothing about a topic either way.
  const needsWork = topics.filter((t) => t.n >= 3 && t.pct < 70)
    .sort((a, b) => a.pct - b.pct || b.n - a.n).slice(0, 3);
  const strong = topics.filter((t) => t.n >= 5 && t.pct >= 90)
    .sort((a, b) => b.n - a.n).slice(0, 3);

  // A few real misses, with answers only where they mean something on their
  // own (a typed number or word, not an option letter).
  const missed = thisQa.filter((r) => !r.correct && r.question_text).slice(-5).map((r) => {
    // A spelling prompt is "Spell the word you hear" - the word is the point.
    if (r.subject === "Spelling" && r.correct_answer) {
      return { subject: r.subject, text: `Spelling: ${r.correct_answer}`,
               yourAnswer: r.your_answer ? String(r.your_answer) : null, correctAnswer: String(r.correct_answer) };
    }
    const showable = r.your_answer && r.correct_answer &&
      !LETTERS_ONLY.test(String(r.your_answer)) && !LETTERS_ONLY.test(String(r.correct_answer));
    return { subject: r.subject, text: String(r.question_text).slice(0, 220),
             yourAnswer: showable ? String(r.your_answer) : null,
             correctAnswer: showable ? String(r.correct_answer) : null };
  });

  const added = imports.filter((r) => r.status === "published" && inRange(r.created_at, week.start, week.end))
    .map((r) => r.kind === "worksheet"
      ? `${r.question_count ?? "New"} questions from "${r.assignment}"`
      : `${r.word_count ?? "New"} spelling words${r.group_name ? ` (${r.group_name} group)` : ""}`);

  return {
    weekOf: week.weekOf, days: week.days,
    sessions: sessions.length,
    unfinished: sessions.filter((s) => s.abandoned).length,
    minutes: Math.round(Object.values(minutesByDay).reduce((a, b) => a + b, 0)),
    daysPractised: Object.values(sessionsByDay).filter((n) => n > 0).length,
    minutesByDay, questions, accuracy: pct(correct, questions),
    subjects, needsWork, strong, missed, added,
  };
}

// ── The email ────────────────────────────────────────────────────────────
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];
const fmtDay = (iso) => { const [, m, d] = iso.split("-").map(Number); return `${MONTHS[m - 1]} ${d}`; };

function trend(s) {
  if (s.prevPct == null || s.pct == null) return "";
  const d = s.pct - s.prevPct;
  if (Math.abs(d) < 3) return " (about the same as last week)";
  return d > 0 ? ` (up from ${s.prevPct}%)` : ` (down from ${s.prevPct}%)`;
}

/** { subject, text, html } for one parent. */
export function renderEmail(sum, { student, parentName, appUrl }) {
  const range = `${fmtDay(sum.days[0])} – ${fmtDay(sum.days[6])}`;
  const subject = sum.sessions
    ? `${student}'s practice, ${range}: ${sum.sessions} session${sum.sessions === 1 ? "" : "s"}, ${sum.accuracy}% correct`
    : `${student}'s practice, ${range}: no practice recorded`;
  const hi = parentName ? `Hi ${parentName},` : "Hi,";

  const lines = [hi, ""];
  if (!sum.sessions) {
    lines.push(`${student} didn't finish any practice sessions this week.`);
  } else {
    lines.push(`${student} practised on ${sum.daysPractised} of 7 days: ${sum.sessions} session${sum.sessions === 1 ? "" : "s"}, ` +
      `about ${sum.minutes} minutes, ${sum.questions} questions, ${sum.accuracy}% correct.`);
    if (sum.unfinished) lines.push(`${sum.unfinished} of those sessions were left before the end.`);
    lines.push("", "By subject:");
    for (const s of sum.subjects) lines.push(`  ${s.subject}: ${s.pct}% of ${s.n} questions${trend(s)}`);
    if (sum.needsWork.length) {
      lines.push("", "Needs more work:");
      for (const t of sum.needsWork) lines.push(`  ${t.topic} (${t.subject}): ${t.pct}% of ${t.n}`);
    }
    if (sum.strong.length) {
      lines.push("", "Going well:");
      for (const t of sum.strong) lines.push(`  ${t.topic} (${t.subject}): ${t.pct}% of ${t.n}`);
    }
    if (sum.missed.length) {
      lines.push("", "Some questions missed:");
      for (const m of sum.missed) {
        lines.push(`  - ${m.text}` + (m.correctAnswer ? ` (answered ${m.yourAnswer}, correct: ${m.correctAnswer})` : ""));
      }
    }
  }
  if (sum.added.length) lines.push("", "Added to the app this week:", ...sum.added.map((a) => `  - ${a}`));
  if (appUrl) lines.push("", `Open the app: ${appUrl}`);
  const text = lines.join("\n");

  const cell = "padding:6px 10px;border-bottom:1px solid #e5e7eb;";
  const dayBars = sum.days.map((d, i) => {
    const m = Math.round(sum.minutesByDay[d] || 0);
    return `<td style="text-align:center;padding:4px;font-size:12px;color:${m ? "#111827" : "#9ca3af"}">
      <div style="font-weight:700">${m ? m + "m" : "–"}</div><div>${WEEKDAYS[i]}</div></td>`;
  }).join("");
  const table = (rows) => `<table style="border-collapse:collapse;width:100%;font-size:14px">${rows}</table>`;
  const section = (title, body) => `<h3 style="font-size:15px;margin:22px 0 6px">${title}</h3>${body}`;

  let body = `<p>${esc(hi)}</p>`;
  if (!sum.sessions) {
    body += `<p>${esc(student)} didn't finish any practice sessions this week.</p>`;
  } else {
    body += `<p><b>${sum.sessions}</b> session${sum.sessions === 1 ? "" : "s"} on <b>${sum.daysPractised}</b> of 7 days ·
      about <b>${sum.minutes}</b> minutes · <b>${sum.questions}</b> questions · <b>${sum.accuracy}%</b> correct` +
      (sum.unfinished ? `<br><span style="color:#6b7280">${sum.unfinished} left before the end</span>` : "") + `</p>
      <table style="border-collapse:collapse;margin:8px 0"><tr>${dayBars}</tr></table>`;
    body += section("By subject", table(sum.subjects.map((s) =>
      `<tr><td style="${cell}">${esc(s.subject)}</td><td style="${cell}text-align:right"><b>${s.pct}%</b> of ${s.n}</td>
       <td style="${cell}color:#6b7280">${esc(trend(s).replace(/^ \(|\)$/g, ""))}</td></tr>`).join("")));
    if (sum.needsWork.length) body += section("Needs more work", table(sum.needsWork.map((t) =>
      `<tr><td style="${cell}">${esc(t.topic)} <span style="color:#6b7280">${esc(t.subject)}</span></td>
       <td style="${cell}text-align:right;color:#b91c1c"><b>${t.pct}%</b> of ${t.n}</td></tr>`).join("")));
    if (sum.strong.length) body += section("Going well", table(sum.strong.map((t) =>
      `<tr><td style="${cell}">${esc(t.topic)} <span style="color:#6b7280">${esc(t.subject)}</span></td>
       <td style="${cell}text-align:right;color:#15803d"><b>${t.pct}%</b> of ${t.n}</td></tr>`).join("")));
    if (sum.missed.length) body += section("Some questions missed", `<ul style="padding-left:18px;margin:0">${sum.missed.map((m) =>
      `<li style="margin:6px 0;white-space:pre-line">${esc(m.text)}` +
      (m.correctAnswer ? `<br><span style="color:#6b7280">Answered ${esc(m.yourAnswer)} · correct: <b>${esc(m.correctAnswer)}</b></span>` : "") +
      `</li>`).join("")}</ul>`);
  }
  if (sum.added.length) body += section("Added to the app this week",
    `<ul style="padding-left:18px;margin:0">${sum.added.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>`);
  if (appUrl) body += `<p style="margin-top:24px"><a href="${esc(appUrl)}">Open the app</a></p>`;

  const html = `<!doctype html><html><body style="margin:0;background:#f9fafb">
<div style="max-width:560px;margin:0 auto;padding:20px 16px;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#111827;background:#fff">
<h2 style="font-size:18px;margin:0 0 4px">${esc(student)}'s week of practice</h2>
<div style="color:#6b7280;font-size:13px;margin-bottom:12px">${esc(range)}</div>
${body}
</div></body></html>`;
  return { subject, text, html };
}
