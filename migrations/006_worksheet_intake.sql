-- Worksheets emailed in (worksheet-intake) share intake_runs with spelling.
--
-- A worksheet run has a lifecycle spelling does not: the questions are
-- model-written, so they are inserted inactive and wait for a parent.
--   processing -> review -> published | discarded
--   processing -> failed
-- `question_ids` is what Publish flips to active (or Discard leaves off).
ALTER TABLE intake_runs
  ADD COLUMN IF NOT EXISTS kind           text NOT NULL DEFAULT 'spelling',
  ADD COLUMN IF NOT EXISTS subject        text,
  ADD COLUMN IF NOT EXISTS assignment     text,
  ADD COLUMN IF NOT EXISTS question_count integer,
  ADD COLUMN IF NOT EXISTS question_ids   jsonb,
  ADD COLUMN IF NOT EXISTS source_hash    text;

ALTER TABLE intake_runs DROP CONSTRAINT IF EXISTS intake_runs_status_check;
ALTER TABLE intake_runs ADD CONSTRAINT intake_runs_status_check
  CHECK (status IN ('published','failed','ignored','duplicate','processing','review','discarded'));

ALTER TABLE intake_runs DROP CONSTRAINT IF EXISTS intake_runs_kind_check;
ALTER TABLE intake_runs ADD CONSTRAINT intake_runs_kind_check
  CHECK (kind IN ('spelling','worksheet'));

CREATE INDEX IF NOT EXISTS idx_intake_runs_hash ON intake_runs(kind, source_hash);
