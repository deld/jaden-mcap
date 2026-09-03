-- ============================================================
-- Migration: separate regular classwork from standardized test prep
--
-- `source` already exists but describes PROVENANCE
-- ('manual' | 'packet' | 'ai-generated'). A scanned worksheet and a
-- scanned MCAP page are both 'packet', so it cannot express PURPOSE.
-- `track` is the orthogonal dimension.
-- ============================================================

ALTER TABLE questions
  ADD COLUMN IF NOT EXISTS track      text NOT NULL DEFAULT 'test_prep',
  ADD COLUMN IF NOT EXISTS assignment text;

-- Every existing question is MCAP material, so the default backfills correctly.
UPDATE questions SET track = 'test_prep' WHERE track IS NULL;

ALTER TABLE questions
  DROP CONSTRAINT IF EXISTS questions_track_check;
ALTER TABLE questions
  ADD CONSTRAINT questions_track_check CHECK (track IN ('test_prep','classwork'));

CREATE INDEX IF NOT EXISTS idx_questions_track ON questions(grade, track, subject);

-- Sessions record which track they belong to so progress and the parent
-- dashboard can report classwork and test prep separately.
ALTER TABLE attempts
  ADD COLUMN IF NOT EXISTS track text NOT NULL DEFAULT 'test_prep';

CREATE INDEX IF NOT EXISTS idx_attempts_track ON attempts(student, track, created_at DESC);
