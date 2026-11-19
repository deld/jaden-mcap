-- Recorded readings of spelling words, made by spelling-media / spelling-intake
-- with OpenAI text-to-speech: <word>/full.mp3 (word - sentence - word, the way
-- the teacher reads a test) and <word>/word.mp3 (the word alone).
--
-- PUBLIC, unlike the worksheets bucket: these are spoken spelling words and
-- sentences, nothing personal, and Jaden plays them without signing in. Only
-- the service role writes here (no insert/update policy for anyone else).
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('spelling-audio', 'spelling-audio', true, 2097152, ARRAY['audio/mpeg'])
ON CONFLICT (id) DO NOTHING;
