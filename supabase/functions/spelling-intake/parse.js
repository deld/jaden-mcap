// ─────────────────────────────────────────────────────────────────────────
// Parsing a teacher's weekly spelling doc.
//
// The doc's shape is controlled by the teacher and can change week to week,
// so every function here is deliberately STRICT: it either returns a result
// it is confident about, or throws with a reason. A silent wrong guess would
// put the wrong spelling words in front of a child, which is worse than an
// import that visibly fails.
//
// We fetch the HTML export rather than the txt export because a Google Docs
// table collapses into undifferentiated lines in plain text - the column
// structure we need to find one group's word list is lost.
// ─────────────────────────────────────────────────────────────────────────

const ENTITIES = {
  "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
  "&#39;": "'", "&apos;": "'", "&nbsp;": " ",
};

export function stripTags(html) {
  return html
    .replace(/<[^>]*>/g, " ")
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(Number(d)))
    .replace(/&[a-z]+;|&#39;/gi, (m) => ENTITIES[m.toLowerCase()] ?? m)
    .replace(/\s+/g, " ")
    .trim();
}

/** Every table in the document, as a grid of trimmed cell strings. */
export function extractTables(html) {
  const tables = [];
  for (const t of html.match(/<table[\s\S]*?<\/table>/gi) ?? []) {
    const rows = [];
    for (const r of t.match(/<tr[\s\S]*?<\/tr>/gi) ?? []) {
      const cells = (r.match(/<t[dh][\s\S]*?<\/t[dh]>/gi) ?? []).map(stripTags);
      if (cells.length) rows.push(cells);
    }
    if (rows.length) tables.push(rows);
  }
  return tables;
}

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");

/**
 * Find the student's group from a roster table.
 * Handles both layouts seen in practice: a two-column name|group table, and
 * a table whose column HEADERS are group names with student names beneath.
 */
export function findStudentGroup(tables, student) {
  const target = norm(student);

  // Layout A: a row containing the student's name; the group is another cell.
  for (const rows of tables) {
    for (const row of rows) {
      const hit = row.findIndex((c) => norm(c) === target || norm(c).startsWith(target + " ".trim()));
      if (hit >= 0) {
        const other = row.filter((_, i) => i !== hit).map((c) => c.trim()).filter(Boolean);
        if (other.length === 1 && other[0].length <= 20) return other[0];
      }
    }
  }

  // Layout B: group names as headers, students listed underneath.
  for (const rows of tables) {
    if (rows.length < 2) continue;
    const header = rows[0];
    for (let c = 0; c < header.length; c++) {
      for (let r = 1; r < rows.length; r++) {
        const cell = rows[r][c];
        if (cell && norm(cell) === target && header[c].trim()) return header[c].trim();
      }
    }
  }

  throw new Error(`Could not find "${student}" in any roster table`);
}

/** A group matches a column header if either contains the other, e.g. "Sky" ⊂ "Sky/Sea". */
export function headerMatchesGroup(header, group) {
  const h = norm(header), g = norm(group);
  if (!h || !g) return false;
  if (h === g) return true;
  // split combined headers like "Sky/Sea" or "Sky & Sea"
  const parts = header.split(/[\/,&+]|\bor\b|\band\b/i).map(norm).filter(Boolean);
  return parts.includes(g) || h.includes(g) || g.includes(h);
}

const WORD_RE = /^[a-z][a-z'-]{1,24}$/i;

export function looksLikeWord(s) {
  const t = s.trim();
  return WORD_RE.test(t) && !/^(word|words|list|group|name|student|sun|sky|sea|green)$/i.test(t);
}

/**
 * Pull one group's word list out of the word table.
 * Throws unless the result is confidently a word list.
 */
export function extractWordList(tables, group) {
  const MIN_WORDS = 8, MAX_WORDS = 40;

  for (const rows of tables) {
    if (rows.length < 2) continue;
    const header = rows[0];
    const col = header.findIndex((h) => headerMatchesGroup(h, group));
    if (col < 0) continue;

    const words = [];
    for (let r = 1; r < rows.length; r++) {
      const cell = (rows[r][col] ?? "").trim();
      if (!cell) continue;
      // A cell may hold several words separated by commas or line breaks.
      for (const part of cell.split(/[,;\n]/).map((p) => p.trim()).filter(Boolean)) {
        if (looksLikeWord(part)) words.push(part.toLowerCase());
      }
    }

    const unique = [...new Set(words)];
    if (unique.length < MIN_WORDS) {
      throw new Error(
        `Found column "${header[col]}" for group "${group}" but only ${unique.length} usable words (need at least ${MIN_WORDS})`,
      );
    }
    if (unique.length > MAX_WORDS) {
      throw new Error(`Column "${header[col]}" yielded ${unique.length} words, more than the ${MAX_WORDS} expected`);
    }
    return { group, words: unique, columnHeader: header[col] };
  }

  const headers = tables.filter((t) => t.length).map((t) => t[0].join(" | ")).join("  //  ");
  throw new Error(`No column matched group "${group}". Headers seen: ${headers}`);
}

/** The first Google Docs link in an email body. */
export function findDocLink(text) {
  const m = text.match(/https?:\/\/docs\.google\.com\/document\/d\/([A-Za-z0-9_-]{20,})/);
  if (!m) throw new Error("No Google Docs link found in the email body");
  return `https://docs.google.com/document/d/${m[1]}/export?format=html`;
}

export function parseSpellingDoc(html, student) {
  const tables = extractTables(html);
  if (!tables.length) throw new Error("No tables found in the document export");
  const group = findStudentGroup(tables, student);
  return extractWordList(tables, group);
}
