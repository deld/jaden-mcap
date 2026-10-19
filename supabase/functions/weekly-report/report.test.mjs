// Tests for the weekly report. Run: node supabase/functions/weekly-report/report.test.mjs
import assert from 'node:assert/strict';
import { lastFullWeek, zonedMidnight, localDay, summarize, renderEmail } from './report.js';

let pass = 0, fail = 0;
const t = (name, fn) => { try { fn(); pass++; console.log('  ok   ' + name); }
                          catch (e) { fail++; console.log('  FAIL ' + name + '\n       ' + e.message); } };

console.log('report.js');

// ── weeks, in Eastern time ──
t('Monday 7am Eastern reports the Mon-Sun that just ended', () => {
  const w = lastFullWeek(new Date('2026-10-19T11:00:00Z'));  // Mon Oct 19, 7am EDT
  assert.equal(w.weekOf, '2026-10-12');
  assert.deepEqual([w.days[0], w.days[6]], ['2026-10-12', '2026-10-18']);
  assert.equal(w.start.toISOString(), '2026-10-12T04:00:00.000Z');  // midnight EDT
  assert.equal(w.end.toISOString(), '2026-10-19T04:00:00.000Z');
});
t('a Sunday run still reports the last COMPLETE week, not the one in progress', () => {
  assert.equal(lastFullWeek(new Date('2026-10-18T23:00:00Z')).weekOf, '2026-10-05');
});
t('late Sunday night Eastern is still Sunday, even though it is Monday in UTC', () => {
  // 11:30pm EDT Sun Oct 18 = 03:30Z Mon Oct 19
  assert.equal(lastFullWeek(new Date('2026-10-19T03:30:00Z')).weekOf, '2026-10-05');
  assert.equal(localDay('2026-10-19T03:30:00Z'), '2026-10-18');
});
t('the week the clocks change is 7 local days, not 7 x 24 hours', () => {
  const w = lastFullWeek(new Date('2026-11-09T12:00:00Z'));  // covers Nov 1 (DST ends)
  assert.equal(w.start.toISOString(), '2026-11-02T05:00:00.000Z');
  assert.equal(zonedMidnight(2026, 11, 1).toISOString(), '2026-11-01T04:00:00.000Z');  // still EDT at midnight
});

// ── summarising ──
const week = lastFullWeek(new Date('2026-10-19T11:00:00Z'));
const at = (day, hour = 16) => new Date(Date.UTC(2026, 9, day, hour)).toISOString();  // 16Z = noon EDT
const session = (day, over = {}) => ({ created_at: at(day), total: 10, score: 8, time_sec: 600,
                                       completed: true, abandoned: false, ...over });
const q = (day, subject, correct, over = {}) => ({ created_at: at(day), subject, domain: 'NF', category: 'Fractions',
                                                   correct, question_text: 'What is 3/4 + 1/4?', ...over });

t('counts only sessions that ended with answers, inside the week', () => {
  const s = summarize({ week, attempts: [
    session(12), session(14, { abandoned: true, completed: false, total: 4, score: 2, time_sec: 120 }),
    session(15, { completed: false, abandoned: false }),       // still open: not counted
    session(16, { total: 0, score: 0 }),                       // ended with nothing: not counted
    session(19), session(11),                                  // next week / last week
  ] });
  assert.equal(s.sessions, 2);
  assert.equal(s.unfinished, 1);
  assert.equal(s.questions, 14);
  assert.equal(s.accuracy, 71);
  assert.equal(s.minutes, 12);
  assert.equal(s.daysPractised, 2);
  assert.equal(Math.round(s.minutesByDay['2026-10-12']), 10);
});
t('subject accuracy comes from question rows, with last week for comparison', () => {
  const qa = [
    ...Array.from({ length: 10 }, (_, i) => q(13, 'Math', i < 9)),        // this week 90%
    ...Array.from({ length: 10 }, (_, i) => q(6, 'Math', i < 6)),         // last week 60%
    q(13, 'Reading', true, { domain: 'RL', category: null }),
  ];
  const s = summarize({ week, qa, attempts: [session(13)] });
  const math = s.subjects.find(x => x.subject === 'Math');
  assert.deepEqual([math.pct, math.prevPct, math.n], [90, 60, 10]);
  assert.equal(s.subjects.find(x => x.subject === 'Reading').prevPct, null);
});
t('weak topics need at least 3 tries; strong ones at least 5', () => {
  const qa = [
    q(13, 'Math', false, { category: 'Division' }), q(13, 'Math', false, { category: 'Division' }),  // 2 tries: too few
    ...[false, false, true].map(c => q(13, 'Math', c, { category: 'Mixed Numbers' })),             // 33% of 3
    ...Array.from({ length: 5 }, () => q(13, 'Math', true, { category: 'Multiplication' })),        // 100% of 5
  ];
  const s = summarize({ week, qa, attempts: [session(13)] });
  assert.deepEqual(s.needsWork.map(x => x.topic), ['Mixed Numbers']);
  assert.deepEqual(s.strong.map(x => x.topic), ['Multiplication']);
});
t('falls back to the domain name when a question has no category', () => {
  const qa = [false, false, false].map(c => q(13, 'Reading', c, { domain: 'RI', category: null }));
  assert.equal(summarize({ week, qa }).needsWork[0].topic, 'Informational Text');
});
t('missed questions show typed answers but not bare option letters', () => {
  const qa = [
    q(13, 'Math', false, { your_answer: '12', correct_answer: '14' }),
    q(13, 'Math', false, { your_answer: 'B', correct_answer: 'C' }),
  ];
  const [typed, letter] = summarize({ week, qa }).missed;
  assert.deepEqual([typed.yourAnswer, typed.correctAnswer], ['12', '14']);
  assert.equal(letter.correctAnswer, null);
});
t('spelling shows as "Weekly words" and a miss names the word, not the prompt', () => {
  const qa = [false, false, true].map((c, i) => q(13, 'Spelling', c, { domain: 'Words Their Way', category: 'Sky',
    question_text: 'Spell the word you hear. ___ (9 letters)', your_answer: 'microwav', correct_answer: 'microwave' }));
  const s = summarize({ week, qa });
  assert.equal(s.needsWork[0].topic, 'Weekly words');
  assert.deepEqual(s.missed[0], { subject: 'Spelling', text: 'Spelling: microwave', yourAnswer: 'microwav', correctAnswer: 'microwave' });
});
t('lists what was imported that week', () => {
  const s = summarize({ week, imports: [
    { status: 'published', created_at: at(13), kind: 'spelling', word_count: 23, group_name: 'Sky' },
    { status: 'published', created_at: at(14), kind: 'worksheet', question_count: 12, assignment: 'Oct 14 Fractions' },
    { status: 'failed', created_at: at(14), kind: 'spelling' },
  ] });
  assert.deepEqual(s.added, ['23 spelling words (Sky group)', '12 questions from "Oct 14 Fractions"']);
});

// ── the email ──
t('a week with practice: subject line and text carry the headline numbers', () => {
  const s = summarize({ week, attempts: [session(12), session(13)], qa: [q(12, 'Math', true)] });
  const e = renderEmail(s, { student: 'Jaden', parentName: 'Delali' });
  assert.equal(e.subject, "Jaden's practice, Oct 12 – Oct 18: 2 sessions, 80% correct");
  assert.match(e.text, /^Hi Delali,/);
  assert.match(e.text, /practised on 2 of 7 days/);
  assert.match(e.html, /<b>80%<\/b> correct/);
});
t('a week with no practice says so plainly', () => {
  const e = renderEmail(summarize({ week }), { student: 'Jaden' });
  assert.match(e.subject, /no practice recorded/);
  assert.match(e.text, /didn't finish any practice sessions/);
});
t('question text is escaped in the HTML', () => {
  const s = summarize({ week, attempts: [session(13)], qa: [q(13, 'Math', false, { question_text: 'Is 3 < 5 & 5 > 2?' })] });
  const { html } = renderEmail(s, { student: 'Jaden' });
  assert.ok(html.includes('Is 3 &lt; 5 &amp; 5 &gt; 2?'));
  assert.ok(!html.includes('3 < 5'));
});
t('the app link appears only when configured', () => {
  const s = summarize({ week });
  assert.ok(!renderEmail(s, { student: 'Jaden' }).html.includes('Open the app'));
  assert.ok(renderEmail(s, { student: 'Jaden', appUrl: 'https://x.test/' }).text.includes('https://x.test/'));
});

console.log(`\n${pass} passed, ${fail} failed`);
if (fail) process.exit(1);
