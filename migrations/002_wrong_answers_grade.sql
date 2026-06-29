-- Add grade column to wrong_answers so wrong answers are isolated per grade
ALTER TABLE wrong_answers
  ADD COLUMN IF NOT EXISTS grade integer NOT NULL DEFAULT 3;

UPDATE wrong_answers SET grade = 3 WHERE grade IS NULL;

CREATE INDEX IF NOT EXISTS idx_wrong_answers_grade ON wrong_answers(student, grade, subject);
