// Tests for the spelling sentence helpers. Run: node supabase/functions/_shared/sentences.test.mjs
import assert from 'node:assert/strict';
import { isPlaceholder, checkSentence, toCloze, spokenScript, audioPath, acceptSentences, sentencePrompt } from './sentences.js';

let pass = 0, fail = 0;
const t = (name, fn) => { try { fn(); pass++; console.log('  ok   ' + name); }
                          catch (e) { fail++; console.log('  FAIL ' + name + '\n       ' + e.message); } };
console.log('sentences.js');

t('recognises the old stand-in text', () => {
  assert.ok(isPlaceholder('Spell the word you hear. ___ (6 letters)'));
  assert.ok(!isPlaceholder('The doctor tapped my knee to test my ___.'));
});
t('a good sentence passes', () => {
  assert.equal(checkSentence('reflex', 'The doctor tapped my knee to test my reflex.'), null);
});
t('the word must appear exactly once, in exactly that form', () => {
  assert.match(checkSentence('reflex', 'The doctor tested my reflexes with a small hammer.'), /does not use/);
  assert.match(checkSentence('object', 'I object to the object on the table today.'), /2 times/);
  assert.match(checkSentence('admit', 'She was admitted to the club after school today.'), /does not use/);
});
t('matching ignores capitals but not word boundaries', () => {
  assert.equal(checkSentence('eject', 'Eject the disc before you turn off the old player.'), null);
  assert.match(checkSentence('mit', 'I will submit my homework to the teacher on Friday.'), /does not use/);
});
t('length and shape are checked', () => {
  assert.match(checkSentence('motion', 'Motion is good.'), /too short/);
  assert.match(checkSentence('motion', 'The ' + 'very '.repeat(20) + 'slow motion replay showed the goal.'), /too long/);
  assert.match(checkSentence('motion', 'The slow motion replay showed the winning goal'), /end like a sentence/);
  assert.match(checkSentence('motion', 'The slow motion replay showed the ___ goal today.'), /blank/);
});
t('the cloze blanks the word and nothing else', () => {
  assert.equal(toCloze('reflex', 'The doctor tapped my knee to test my reflex.'), 'The doctor tapped my knee to test my ___.');
  assert.equal(toCloze('eject', 'Eject the disc before you turn off the player.'), '___ the disc before you turn off the player.');
});
t('the voice reads word, sentence, word', () => {
  assert.equal(spokenScript('reflex', 'Test my reflex.'), 'reflex.\n\nTest my reflex.\n\nreflex.');
  assert.equal(spokenScript('reflex', ''), 'reflex.');
});
t('audio paths are per word and safe', () => {
  assert.equal(audioPath('Reflex', 'full'), 'reflex/full.mp3');
  assert.equal(audioPath("o'clock", 'word'), "o'clock/word.mp3");
});
t('keeps good sentences and reports the rest', () => {
  const { ok, bad } = acceptSentences(['reflex', 'admit', 'motion'], { sentences: [
    { word: 'reflex', sentence: 'The doctor tapped my knee to test my reflex.' },
    { word: 'Admit', sentence: 'He was admitted to the team after the tryout.' },
  ] });
  assert.deepEqual(Object.keys(ok), ['reflex']);
  assert.deepEqual(bad.map(b => b.word), ['admit', 'motion']);
  assert.match(bad[1].reason, /no sentence/);
});
t('the prompt lists every word', () => {
  const p = sentencePrompt(['reflex', 'admit']);
  assert.ok(p.includes('- reflex') && p.includes('- admit') && /EXACTLY/.test(p));
});

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
