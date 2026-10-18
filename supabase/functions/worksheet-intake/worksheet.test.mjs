// Tests for the worksheet-intake helpers. Run: node supabase/functions/worksheet-intake/worksheet.test.mjs
import assert from 'node:assert/strict';
import {
  triage, pickAttachments, checkQuestion, agrees, reconcile, checkWorksheet,
  assignmentName, toRows, solverView, parseNumber, GENERATE_SCHEMA,
} from './worksheet.js';

let pass = 0, fail = 0;
const t = (name, fn) => { try { fn(); pass++; console.log('  ok   ' + name); }
                          catch (e) { fail++; console.log('  FAIL ' + name + '\n       ' + e.message); } };

const big = 'A'.repeat(40_000);  // ~30 KB once decoded: a real page, not a logo
const mc = (over = {}) => ({
  type: 'single', category: 'Mixed Numbers', text: 'Write a mixed number: 2 wholes and 3 fourths',
  options: ['2 3/4', '3 2/4', '2 4/3', '5 3/4'], answer: '2 3/4',
  hint: 'Wholes first.', solution: '2 wholes and 3 of 4 parts.\nThat is 2 3/4.', ...over,
});
const num = (over = {}) => ({
  type: 'numeric', category: 'Multiplication', text: 'What is 12 x 4?', options: [], answer: '48',
  hint: 'Think 10 x 4 and 2 x 4.', solution: '10 x 4 = 40\n2 x 4 = 8\n40 + 8 = 48', ...over,
});

console.log('worksheet.js');

// ── triage ──
const ALLOWED = ['lt.dzirasa@gmail.com', 'delali.dzirasa@gmail.com'];
t('a known sender gets in', () => {
  assert.equal(triage({ from: 'L T <lt.dzirasa@gmail.com>', allowedFrom: ALLOWED }).process, true);
});
t('anyone else is rejected, even mentioning the school', () => {
  const g = triage({ from: 'stranger@example.com', allowedFrom: ALLOWED });
  assert.equal(g.process, false);
  assert.match(g.detail, /stranger@example\.com/);
});
t('an empty allow-list lets nobody in', () => {
  assert.equal(triage({ from: 'lt.dzirasa@gmail.com', allowedFrom: [''] }).process, false);
});

// ── attachments ──
t('keeps photos and PDFs in order', () => {
  const pages = pickAttachments({ attachments: [
    { file_name: 'p1.jpg', content_type: 'image/jpeg', content: big },
    { file_name: 'packet.pdf', content_type: 'application/pdf', content: 'JVBERi0x' },
  ] });
  assert.deepEqual(pages.map(p => p.mediaType), ['image/jpeg', 'application/pdf']);
});
t('drops signature logos but keeps the page', () => {
  const pages = pickAttachments({ attachments: [
    { file_name: 'logo.png', content_type: 'image/png', content: 'iVBORw0KGgo=' },
    { file_name: 'page.png', content_type: 'image/png', content: big },
  ] });
  assert.deepEqual(pages.map(p => p.name), ['page.png']);
});
t('infers the type from the extension when sent as octet-stream', () => {
  const [p] = pickAttachments({ attachments: [{ file_name: 'IMG_1.JPG', content_type: 'application/octet-stream', content: big }] });
  assert.equal(p.mediaType, 'image/jpeg');
});
t('accepts an attachment-store URL instead of inline content', () => {
  const [p] = pickAttachments({ attachments: [{ file_name: 'a.pdf', content_type: 'application/pdf', url: 'https://x/a.pdf', size: 5000 }] });
  assert.equal(p.url, 'https://x/a.pdf');
});
t('refuses HEIC with instructions instead of skipping it silently', () => {
  assert.throws(() => pickAttachments({ attachments: [{ file_name: 'IMG_2.HEIC', content_type: 'image/heic', content: big }] }),
                /HEIC.*JPEG/);
});
t('refuses an email with nothing usable attached', () => {
  assert.throws(() => pickAttachments({ attachments: [{ file_name: 'notes.docx', content_type: 'application/msword', content: big }] }),
                /No worksheet attached.*notes\.docx/);
  assert.throws(() => pickAttachments({}), /No worksheet attached/);
});
t('refuses more than 25 MB', () => {
  assert.throws(() => pickAttachments({ attachments: [{ file_name: 'a.pdf', content_type: 'application/pdf', url: 'u', size: 30e6 }] }),
                /25 MB/);
});

// ── question checks ──
t('a good multiple-choice question passes', () => assert.equal(checkQuestion(mc()), null));
t('a good numeric question passes', () => assert.equal(checkQuestion(num()), null));
t('numeric answers must be plain numbers the number box accepts', () => {
  assert.match(checkQuestion(num({ answer: '3/4' })), /not a plain number/);
  assert.match(checkQuestion(num({ answer: '48 cm' })), /not a plain number/);
  assert.equal(checkQuestion(num({ answer: '1,200' })), null);
  assert.equal(checkQuestion(num({ answer: '3.5' })), null);
});
t('the answer must be exactly one of the options', () => {
  assert.match(checkQuestion(mc({ answer: '2 1/4' })), /not exactly one/);
});
t('duplicate options are rejected', () => {
  assert.match(checkQuestion(mc({ options: ['2 3/4', '2  3/4', '1', '5'] })), /same/);
});
t('baked-in letter prefixes are rejected (the app draws its own, see #29)', () => {
  assert.match(checkQuestion(mc({ options: ['A. 2 3/4', 'B. 3 2/4', 'C. 2 4/3'], answer: 'A. 2 3/4' })), /letter prefixes/);
});
t('too few or too many options are rejected', () => {
  assert.match(checkQuestion(mc({ options: ['2 3/4', '1'] })), /2 options/);
});
t('a question pointing at a picture Jaden cannot see is rejected', () => {
  assert.match(checkQuestion(mc({ text: 'Look at the model shown above. What mixed number is it?' })), /picture/);
});
t('missing hint or solution is rejected', () => {
  assert.match(checkQuestion(num({ hint: ' ' })), /hint/);
});

// ── independent solve ──
t('agreement is by option text, ignoring case and spacing', () => {
  assert.ok(agrees(mc(), ' 2  3/4 '));
  assert.ok(!agrees(mc(), '3 2/4'));
});
t('numeric agreement is by value', () => {
  assert.ok(agrees(num(), '48.0'));
  assert.ok(!agrees(num(), '47'));
  assert.ok(!agrees(num(), undefined));
});
t('reconcile keeps only checked questions the solver agreed with', () => {
  const qs = [mc(), num(), num({ text: 'What is 7 x 8?', answer: '54' }), mc({ answer: 'nope' })];
  const { kept, dropped } = reconcile(qs, [
    { n: 1, answer: '2 3/4' }, { n: 2, answer: '48' }, { n: 3, answer: '56' }, { n: 4, answer: 'nope' },
  ]);
  assert.equal(kept.length, 2);
  assert.equal(dropped.length, 2);
  assert.match(dropped[0].reason, /solver answered "56", key says "54"/);
});
t('a question the solver skipped is dropped', () => {
  assert.equal(reconcile([mc()], []).kept.length, 0);
});
t('the solver never sees the answers or hints', () => {
  const v = solverView([mc(), num()]);
  assert.ok(!v.includes('Wholes first') && !v.includes('48'));
  assert.ok(v.includes('Question 2:') && v.includes('- 3 2/4'));
});

// ── worksheet-level ──
const sheet = (over = {}) => ({ readable: true, problem: '', subject: 'Math', domain: 'NF',
                                title: 'Fractions', skills: 'x', questions: [mc()], ...over });
t('an unreadable worksheet is refused with the model\'s reason', () => {
  assert.throws(() => checkWorksheet(sheet({ readable: false, problem: 'Too blurry', questions: [] })), /Too blurry/);
});
t('a domain from the wrong subject is refused', () => {
  assert.throws(() => checkWorksheet(sheet({ domain: 'RL' })), /does not belong to Math/);
});
t('the schema only allows the app\'s domains', () => {
  assert.deepEqual(GENERATE_SCHEMA.properties.domain.enum, ['OA', 'NBT', 'NF', 'MD', 'G', 'RL', 'RI', 'L']);
});

// ── naming and rows ──
t('assignment names follow the existing "Sept 23 ..." style', () => {
  assert.equal(assignmentName('Fractions Packet', new Date('2026-09-23T12:00:00Z')), 'Sept 23 Fractions Packet');
});
t('a clashing name gets a number instead of merging two sheets', () => {
  const d = new Date('2026-10-18T12:00:00Z');
  assert.equal(assignmentName('Fractions', d, ['Oct 18 Fractions']), 'Oct 18 Fractions (2)');
  assert.equal(assignmentName('Fractions', d, ['oct 18 fractions', 'Oct 18 Fractions (2)']), 'Oct 18 Fractions (3)');
});
t('rows are inactive classwork with letter keys and numeric values', () => {
  const [a, b] = toRows([mc({ options: ['3 2/4', '2 3/4', '1', '5'] }), num({ answer: '1,200' })],
                        { subject: 'Math', domain: 'NF', assignment: 'Oct 18 Fractions' });
  assert.deepEqual(a.correct, ['B']);
  assert.equal(b.correct, 1200);
  assert.equal(b.options, null);
  for (const r of [a, b]) {
    assert.equal(r.active, false);
    assert.equal(r.track, 'classwork');
    assert.equal(r.assignment, 'Oct 18 Fractions');
    assert.equal(r.grade, 4);
  }
});
t('parseNumber rejects anything the number box would not', () => {
  assert.equal(parseNumber('12'), 12);
  assert.equal(parseNumber('-3.25'), -3.25);
  assert.equal(parseNumber('1/2'), null);
  assert.equal(parseNumber(''), null);
});

console.log(`\n${pass} passed, ${fail} failed`);
if (fail) process.exit(1);
