// Tests for the spelling-doc parser. Run: node supabase/functions/spelling-intake/parse.test.mjs
// The module is TypeScript-only in its types, so strip them for node.
import assert from 'node:assert/strict';
import {
  parseSpellingDoc, findDocLink, headerMatchesGroup, looksLikeWord,
  findStudentGroup, extractTables,
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
const roster = [['Student','Group'], ['Amara','Sun'], ['Jaden','Sky'], ['Noah','Green 1']];
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
  const alt = `<html>${table(wordRows)}${table([['Sun','Green 1','Sky/Sea'], ['Amara','Noah','Jaden']])}</html>`;
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
  assert.throws(() => findDocLink('No link here, see attached PDF'), /No Google Docs link/);
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
