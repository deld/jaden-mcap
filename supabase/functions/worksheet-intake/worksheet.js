// ─────────────────────────────────────────────────────────────────────────
// Pure helpers for worksheet-intake. No network, no Deno: everything here is
// covered by worksheet.test.mjs under plain node.
//
// The function turns a photographed or scanned worksheet into NEW practice
// questions on the same skills - the same thing the upload_*_packet_*.py
// scripts do by hand. The model writes them; this file decides whether what
// it wrote is fit to put in front of Jaden. Like the spelling parser, it is
// strict: a question that fails any check is dropped, and a worksheet that
// leaves too few survivors is refused rather than published thin.
// ─────────────────────────────────────────────────────────────────────────

export const MIN_QUESTIONS = 5;
export const MAX_QUESTIONS = 30;

export const DOMAINS = {
  Math: ["OA", "NBT", "NF", "MD", "G"],
  Reading: ["RL", "RI", "L"],
};

// ── Who gets through the door ────────────────────────────────────────────
// Unlike spelling mail, a worksheet has no school origin to check: it is a
// photo or scan a parent took. So only a known sender gets in. The inbound
// address relays our secret on every message (see the spelling README), so
// the sender check is what keeps a stranger's attachment out.
/** @param {{ from?: string, allowedFrom?: string[] }} [args] */
export function triage({ from = "", allowedFrom = [] } = {}) {
  const fromLc = String(from).toLowerCase();
  if (allowedFrom.some((a) => a && fromLc.includes(a))) {
    return { process: true, detail: "sent by a known sender" };
  }
  return { process: false, detail: `rejected: not from a known sender (from: ${from || "unknown"})` };
}

// ── Attachments ──────────────────────────────────────────────────────────
const IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];
const BY_EXT = {
  pdf: "application/pdf", jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png",
  gif: "image/gif", webp: "image/webp", heic: "image/heic", heif: "image/heif",
};
// Signature logos and tracking pixels ride along on most email. A phone photo
// of a worksheet page is far larger than this.
const MIN_IMAGE_BYTES = 20_000;
const MAX_TOTAL_BYTES = 25_000_000;

const b64Bytes = (b64) => Math.floor((String(b64).replace(/[^A-Za-z0-9+/]/g, "").length * 3) / 4);

function mediaTypeOf(a) {
  const declared = String(a.content_type ?? a.contentType ?? "").toLowerCase().split(";")[0].trim();
  if (declared && declared !== "application/octet-stream") return declared === "image/jpg" ? "image/jpeg" : declared;
  const ext = String(a.file_name ?? a.filename ?? "").toLowerCase().split(".").pop();
  return BY_EXT[ext] ?? declared;
}

/**
 * The worksheet pages in a CloudMailin JSON payload, in the order sent.
 * Each is { name, mediaType, data?, url?, bytes }: `data` is base64 when
 * CloudMailin embeds the file, `url` when an attachment store is configured.
 * Throws with a reason a parent can act on when nothing usable is attached.
 * @returns {{ name: string, mediaType: string, data?: string, url?: string, bytes: number }[]}
 */
export function pickAttachments(payload) {
  const raw = Array.isArray(payload?.attachments) ? payload.attachments : [];
  const pages = [];
  const skipped = [];
  for (const a of raw) {
    const name = String(a.file_name ?? a.filename ?? "attachment");
    const mediaType = mediaTypeOf(a);
    const data = typeof a.content === "string" ? a.content.replace(/\s+/g, "") : undefined;
    const url = typeof a.url === "string" ? a.url : undefined;
    const bytes = Number(a.size) || (data ? b64Bytes(data) : 0);
    if (!data && !url) { skipped.push(`${name}: empty`); continue; }

    if (mediaType === "image/heic" || mediaType === "image/heif") {
      throw new Error(`${name} is an iPhone HEIC photo, which can't be read. ` +
        `Re-send it as a JPEG (in Photos, Share -> Options -> Most Compatible, or Settings -> Camera -> Formats -> Most Compatible).`);
    }
    if (mediaType === "application/pdf") { pages.push({ name, mediaType, data, url, bytes }); continue; }
    if (IMAGE_TYPES.includes(mediaType)) {
      if (bytes && bytes < MIN_IMAGE_BYTES) { skipped.push(`${name}: too small to be a page`); continue; }
      pages.push({ name, mediaType, data, url, bytes });
      continue;
    }
    skipped.push(`${name}: ${mediaType || "unknown type"}`);
  }
  if (!pages.length) {
    throw new Error("No worksheet attached. Send the pages as photos (JPEG/PNG) or a PDF." +
      (skipped.length ? ` Ignored: ${skipped.join("; ")}` : ""));
  }
  const total = pages.reduce((n, p) => n + (p.bytes || 0), 0);
  if (total > MAX_TOTAL_BYTES) {
    throw new Error(`Attachments total ${(total / 1e6).toFixed(1)} MB; the limit is 25 MB. Send fewer or smaller pages.`);
  }
  return pages;
}

// ── What the model is asked for ──────────────────────────────────────────
// Structured outputs guarantee the shape; everything about MEANING (is the
// marked answer one of the options, is a numeric answer a number) is checked
// below, because the schema cannot express it.
const QUESTION_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["type", "category", "text", "options", "answer", "hint", "solution"],
  properties: {
    type: { type: "string", enum: ["single", "numeric"] },
    category: { type: "string" },
    text: { type: "string" },
    options: { type: "array", items: { type: "string" } },
    answer: { type: "string" },
    hint: { type: "string" },
    solution: { type: "string" },
  },
};

export const GENERATE_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["readable", "problem", "subject", "domain", "title", "skills", "questions"],
  properties: {
    readable: { type: "boolean" },
    problem: { type: "string" },
    subject: { type: "string", enum: ["Math", "Reading"] },
    domain: { type: "string", enum: [...DOMAINS.Math, ...DOMAINS.Reading] },
    title: { type: "string" },
    skills: { type: "string" },
    questions: { type: "array", items: QUESTION_SCHEMA },
  },
};

export const SOLVE_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["answers"],
  properties: {
    answers: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["n", "answer"],
        properties: { n: { type: "integer" }, answer: { type: "string" } },
      },
    },
  },
};

export const GENERATE_PROMPT = `You are preparing practice for Jaden, a 4th grader in Maryland, from a worksheet his teacher sent home. The attached pages are the worksheet.

Write NEW practice questions that exercise the same skills as the worksheet, the way a teacher would write a second worksheet: different numbers, different names and contexts, same kind of thinking. Do not copy the worksheet's own problems, and do not copy its reading passages - write short original passages instead.

Rules for every question:
- It must stand on its own as text. Jaden will not see the worksheet or any picture. If the skill uses a model or diagram, describe it in words (e.g. "Write a mixed number: 2 wholes and 3 fourths").
- type "single": 3 to 5 options, exactly one correct. Options are plain text with no "A." or "B)" prefixes. Every wrong option is a mistake a 4th grader would plausibly make, and is definitely wrong. "answer" is the exact text of the correct option.
- type "numeric": Jaden types a number into a number box, so "answer" must be a plain number such as 42 or 3.5 - no units, no commas, no fractions. "options" is []. If the answer is a fraction or mixed number, use "single" instead.
- "category" is a short topic name such as "Mixed Numbers" or "Main Idea"; reuse the same name for questions on the same skill.
- "hint" nudges without giving the answer away. "solution" shows the working in short lines a 9-year-old can follow, separated by newlines.
- Reading questions quote the passage they ask about inside "text", starting with "Read: '...'".

Write between 10 and 20 questions, roughly in the worksheet's order, covering each skill it practises.

"title" names the worksheet the way a parent would, in 2-5 words, such as "Fractions Exercises 20-23" or "Main Idea Practice". "skills" is one or two sentences on what the worksheet covers. "domain" is the Common Core domain that fits best (Math: OA, NBT, NF, MD, G; Reading: RL, RI, L).

If the pages are not a school worksheet, or are too blurry, cropped or dark to read reliably, set "readable" to false, explain why in "problem", and return no questions. Otherwise set "readable" to true and "problem" to "".`;

export const SOLVE_PROMPT = `Below are practice questions for a 4th grader. Solve each one independently and carefully.

For a question with options, answer with the exact text of the one correct option. For a question without options, answer with a plain number only.

Return one answer per question, with "n" set to the question's number.`;

/** The questions as the solver sees them: numbered, no answers, no hints. */
export function solverView(questions) {
  return questions.map((q, i) => {
    const opts = q.type === "single" ? "\nOptions:\n" + q.options.map((o) => `- ${o}`).join("\n") : "\n(Answer with a number.)";
    return `Question ${i + 1}:\n${q.text}${opts}`;
  }).join("\n\n");
}

// ── Checking what came back ──────────────────────────────────────────────
const squash = (s) => String(s ?? "").trim().replace(/\s+/g, " ").toLowerCase();
const LETTER_PREFIX = /^\(?[A-Ha-h][.):]\s+/;
// Questions that lean on something Jaden cannot see.
const NEEDS_PICTURE = /\b(the|this) (picture|diagram|figure|model|graph|chart|image|table) (above|below|shown)\b|\bshown (above|below)\b|\bon the worksheet\b|\bsee (the )?(picture|diagram|figure)\b/i;

export function parseNumber(s) {
  const t = String(s ?? "").trim().replace(/,/g, "");
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  return Number(t);
}

/** A failure reason for one generated question, or null if it is usable. */
export function checkQuestion(q) {
  if (!q || typeof q !== "object") return "not a question";
  for (const k of ["text", "category", "hint", "solution"]) {
    if (!String(q[k] ?? "").trim()) return `missing ${k}`;
  }
  if (NEEDS_PICTURE.test(q.text)) return "refers to a picture Jaden cannot see";

  if (q.type === "numeric") {
    if (parseNumber(q.answer) === null) return `numeric answer "${q.answer}" is not a plain number`;
    return null;
  }
  if (q.type !== "single") return `unknown type "${q.type}"`;

  const opts = Array.isArray(q.options) ? q.options.map((o) => String(o).trim()) : [];
  if (opts.length < 3 || opts.length > 5) return `${opts.length} options (need 3-5)`;
  if (opts.some((o) => !o)) return "an option is blank";
  if (opts.filter((o) => LETTER_PREFIX.test(o)).length >= 2) return "options carry A/B/C letter prefixes";
  if (new Set(opts.map(squash)).size !== opts.length) return "two options are the same";
  const hits = opts.filter((o) => squash(o) === squash(q.answer)).length;
  if (hits !== 1) return `answer "${q.answer}" is not exactly one of the options`;
  return null;
}

/** Does the independent solver's answer match the generator's? */
export function agrees(q, solved) {
  if (solved == null) return false;
  if (q.type === "numeric") {
    const a = parseNumber(q.answer), b = parseNumber(solved);
    return a !== null && b !== null && Math.abs(a - b) < 1e-9;
  }
  return squash(q.answer) === squash(solved);
}

/**
 * Keep a question only if it passes every check AND the solver, working
 * blind, reached the same answer. Disagreement does not tell us which side is
 * wrong, so the question goes either way - the same generate-then-solve idea
 * as the packet scripts' `verify`, without a hand-written expression.
 */
export function reconcile(questions, solvedAnswers) {
  const byN = new Map((solvedAnswers ?? []).map((a) => [Number(a.n), a.answer]));
  const kept = [], dropped = [];
  questions.forEach((q, i) => {
    const bad = checkQuestion(q);
    if (bad) { dropped.push({ text: q?.text, reason: bad }); return; }
    const solved = byN.get(i + 1);
    if (!agrees(q, solved)) {
      dropped.push({ text: q.text, reason: `solver answered "${solved ?? "nothing"}", key says "${q.answer}"` });
      return;
    }
    kept.push(q);
  });
  return { kept, dropped };
}

/** Throws if the worksheet-level fields are unusable. */
export function checkWorksheet(out) {
  if (!out || typeof out !== "object") throw new Error("The model returned nothing usable");
  if (!out.readable) throw new Error(`Couldn't read the worksheet: ${out.problem || "no reason given"}`);
  if (!DOMAINS[out.subject]) throw new Error(`Unknown subject "${out.subject}"`);
  if (!DOMAINS[out.subject].includes(out.domain)) {
    throw new Error(`Domain "${out.domain}" does not belong to ${out.subject}`);
  }
  if (!String(out.title ?? "").trim()) throw new Error("No worksheet title");
  if (!Array.isArray(out.questions) || !out.questions.length) throw new Error("No questions were written");
}

// ── Naming and rows ──────────────────────────────────────────────────────
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];

/** "Oct 20 Fractions Exercises 20-23" - how the classwork list groups sheets. */
export function assignmentName(title, date = new Date(), taken = []) {
  const clean = String(title).replace(/\s+/g, " ").trim().slice(0, 60);
  const base = `${MONTHS[date.getUTCMonth()]} ${date.getUTCDate()} ${clean}`;
  const used = new Set(taken.map((t) => String(t).toLowerCase()));
  if (!used.has(base.toLowerCase())) return base;
  for (let n = 2; ; n++) {
    const next = `${base} (${n})`;
    if (!used.has(next.toLowerCase())) return next;
  }
}

const L = "ABCDEFGH";

/**
 * Question rows, inserted INACTIVE. Nothing reaches Jaden until a parent
 * presses Publish in the app, which flips `active`.
 */
export function toRows(questions, { subject, domain, assignment, grade = 4 }) {
  return questions.map((q) => {
    const single = q.type === "single";
    const options = single ? q.options.map((o) => String(o).trim()) : null;
    const correct = single
      ? [L[options.findIndex((o) => squash(o) === squash(q.answer))]]
      : parseNumber(q.answer);
    return {
      grade, subject, domain, category: String(q.category).trim(),
      type: q.type, text: String(q.text).trim(), options, correct,
      hint: String(q.hint).trim(), solution: String(q.solution).trim(),
      active: false, source: "packet", track: "classwork", assignment,
    };
  });
}
