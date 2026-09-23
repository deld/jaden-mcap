// Tests for the spelling-doc parser. Run: node supabase/functions/spelling-intake/parse.test.mjs
// The module is TypeScript-only in its types, so strip them for node.
import assert from 'node:assert/strict';
import {
  parseSpellingDoc, findDocLink, headerMatchesGroup, looksLikeWord,
  findStudentGroup, extractTables, findDocCandidates, docExportUrl, isRosterBoundary,
} from './parse.js';

const cell = (s) => `<td><p>${s}</p></td>`;
const row  = (cs) => `<tr>${cs.map(cell).join('')}</tr>`;
const table = (rows) => `<table>${rows.map(row).join('')}</table>`;

const WORDS = {
  'Sun':     ['cat','dog','sun','run','hat','pig','bed','top','map','cup'],
  'Green 1': ['happy','funny','sunny','penny','jelly','berry','carry','merry','hurry','worry'],
  'Green 2': ['travel','pencil','animal','signal','local','total','metal','pedal','medal','petal'],
  'Sky/Sea': ['microwave','microscope','microbe','megaphone','megabyte','superhero','superstar',
              'hyperactive','hypercritical','supermarket','megadose','microfilm'],
};
const headers = Object.keys(WORDS);
const maxLen = Math.max(...Object.values(WORDS).map(w => w.length));
const wordRows = [headers, ...Array.from({length: maxLen}, (_, i) => headers.map(h => WORDS[h][i] ?? ''))];
const roster = [['Student','Group'], ['Alpha','Sun'], ['Jaden','Sky'], ['Bravo','Green 1']];
const DOC = `<html><body>${table(wordRows)}<p>Roster</p>${table(roster)}</body></html>`;

let pass = 0, fail = 0;
const t = (name, fn) => { try { fn(); pass++; console.log('  ok   ' + name); }
                          catch (e) { fail++; console.log('  FAIL ' + name + '\n       ' + e.message); } };

console.log("parse.js");

t('finds Jaden\'s group from a name|group roster', () => {
  assert.equal(findStudentGroup(extractTables(DOC), 'Jaden'), 'Sky');
});

t('matches "Sky" against the combined "Sky/Sea" column', () => {
  assert.ok(headerMatchesGroup('Sky/Sea', 'Sky'));
  assert.ok(headerMatchesGroup('Sky & Sea', 'Sea'));
  assert.ok(!headerMatchesGroup('Green 1', 'Sky'));
});

t('extracts exactly that group\'s words, not a neighbour\'s', () => {
  const r = parseSpellingDoc(DOC, 'Jaden');
  assert.equal(r.group, 'Sky');
  assert.deepEqual(r.words, WORDS['Sky/Sea']);
  assert.ok(!r.words.includes('happy'), 'leaked a Green 1 word');
});

t('handles a group-headers roster layout', () => {
  const alt = `<html>${table(wordRows)}${table([['Sun','Green 1','Sky/Sea'], ['Alpha','Bravo','Jaden']])}</html>`;
  assert.equal(parseSpellingDoc(alt, 'Jaden').group, 'Sky/Sea');
});

t('REFUSES when the student is not on the roster', () => {
  assert.throws(() => parseSpellingDoc(DOC, 'Zephyr'), /Could not find "Zephyr"/);
});

t('REFUSES when the group has no matching column', () => {
  const noCol = `<html>${table([['Sun','Green 1'], ['cat','happy']])}${table(roster)}</html>`;
  assert.throws(() => parseSpellingDoc(noCol, 'Jaden'), /No column matched group "Sky"/);
});

t('REFUSES a suspiciously short list rather than publishing it', () => {
  const thin = `<html>${table([['Sky/Sea'], ['microwave'], ['microbe']])}${table(roster)}</html>`;
  assert.throws(() => parseSpellingDoc(thin, 'Jaden'), /only 2 usable words/);
});

t('REFUSES a document with no tables at all', () => {
  assert.throws(() => parseSpellingDoc('<html><p>See attached</p></html>', 'Jaden'), /No tables found/);
});

t('ignores header-ish and non-word cells', () => {
  assert.ok(looksLikeWord('microwave'));
  assert.ok(!looksLikeWord('Sky'));
  assert.ok(!looksLikeWord('Word List'));
  assert.ok(!looksLikeWord('12'));
  assert.ok(!looksLikeWord(''));
});

t('splits a cell holding several comma-separated words', () => {
  const packed = `<html>${table([['Sky/Sea'], ['microwave, microscope, microbe'], ['megaphone, megabyte, superhero'],
                                 ['superstar, hyperactive, supermarket']])}${table(roster)}</html>`;
  assert.equal(parseSpellingDoc(packed, 'Jaden').words.length, 9);
});

t('de-duplicates repeated words', () => {
  const dup = `<html>${table([['Sky/Sea'], ...WORDS['Sky/Sea'].map(w => [w]), ['microwave']])}${table(roster)}</html>`;
  assert.equal(parseSpellingDoc(dup, 'Jaden').words.length, WORDS['Sky/Sea'].length);
});

t('pulls the doc link out of an email body and builds an export URL', () => {
  const body = `Hi families,\nThis week's list: https://docs.google.com/document/d/1AbCdEf_GhIjKlMnOpQrStUvWxYz012345/edit?usp=sharing\nThanks!`;
  assert.equal(findDocLink(body),
    'https://docs.google.com/document/d/1AbCdEf_GhIjKlMnOpQrStUvWxYz012345/export?format=html');
});

t('REFUSES an email with no doc link', () => {
  assert.throws(() => findDocLink('No link here, see attached PDF'), /No followable links|No Google Docs link/);
});

// ── Cases taken from the real Week 4 email and doc ────────────────────────
const TRACK = 'http://url7847.email-support.classroomparent.com/ls/click?upn=u001.';
const REAL_EMAIL = `
  <a href="${TRACK}SPELLINGDOC7lmFP6mfmaXSM2FBz9dmLxW8CXdlA1KTqk">Week 4 SPELLING LIST</a>
  <a href="${TRACK}DIRECTORYObUZp72O1ywIBC2BineVEe2FAleDdelL3y">https://bmpcs.classroomparent.com/</a>
  <a href="${TRACK}UNSUBObUZp72O1ywIBC2BineVEe2FAleDdelL3yOWAW">unsubscribe</a>`;

t('ranks the SPELLING LIST tracker above the directory link', () => {
  const c = findDocCandidates(REAL_EMAIL);
  assert.ok(c[0].includes('SPELLINGDOC'), `expected the spelling tracker first, got ${c[0]}`);
});

t('NEVER offers the unsubscribe link as a candidate', () => {
  for (const u of findDocCandidates(REAL_EMAIL)) {
    assert.ok(!u.includes('UNSUB'), 'the unsubscribe tracker must never be followed');
  }
});

t('excludes an unsubscribe link even when only the URL says so', () => {
  const body = '<a href="https://x.test/unsubscribe?u=1">Click here</a><a href="https://x.test/doc">List</a>';
  const c = findDocCandidates(body);
  assert.ok(!c.some(u => /unsubscribe/i.test(u)));
});

t('still finds a bare Google Docs link when the mail has one', () => {
  const url = findDocLink('List: https://docs.google.com/document/d/1qlKouTf6DQvikTZdicYPF3Hc7_R094srdft6lBNbZCc/edit?usp=sharing');
  assert.equal(url, 'https://docs.google.com/document/d/1qlKouTf6DQvikTZdicYPF3Hc7_R094srdft6lBNbZCc/export?format=html');
});

t('docExportUrl rejects a non-doc URL', () => {
  assert.equal(docExportUrl('https://example.com/page'), null);
});

t('stops at the roster boundary in the real single-table layout', () => {
  // words on top, "Groups"/"Students" rows and names underneath - the real shape
  const rows = [
    ['', 'SUN', 'SKY and SEA'],
    ['', 'care', 'microwave'], ['', 'hair', 'microcosm'], ['', 'part', 'microscope'],
    ['', 'fair', 'microbus'],  ['', 'start', 'microfilm'], ['', 'harm', 'microbe'],
    ['', 'pare', 'megaphone'], ['', 'chair', 'megabyte'],  ['', 'wear', 'superhero'],
    ['Groups', 'Sun', 'Sky'],
    ['Students', 'Alpha', 'Jaden'],
    ['', '', 'Charlie'], ['', '', 'Delta'],
  ];
  const html = `<table>${rows.map(row => `<tr>${row.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</table>`;
  const r = parseSpellingDoc(html, 'Jaden');
  // The column header is the combined label; that is what we want, since the
  // words live under it. Sky must still match it.
  assert.ok(headerMatchesGroup(r.columnHeader, 'Sky'), `column ${r.columnHeader} should match Sky`);
  assert.ok(!r.words.includes('jaden'), 'a child\'s name leaked into the word list');
  assert.ok(!r.words.includes('charlie'), 'a child\'s name leaked into the word list');
  assert.ok(r.words.includes('microwave'));
  assert.equal(r.words.length, 9);
});

t('isRosterBoundary spots both a label row and a repeated header', () => {
  assert.ok(isRosterBoundary(['Students', 'Alpha', 'Jaden'], ['SUN', 'SKY and SEA']));
  assert.ok(isRosterBoundary(['', 'SUN', 'SKY and SEA'], ['SUN', 'SKY and SEA']));
  assert.ok(!isRosterBoundary(['', 'care', 'microwave'], ['SUN', 'SKY and SEA']));
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
