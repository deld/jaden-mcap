-- Every run of the spelling-intake webhook, published or not. This is the
-- "notify" half: the app reads it to show what was imported and to surface a
-- refusal loudly instead of failing silently.
CREATE TABLE IF NOT EXISTS intake_runs (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at   timestamptz NOT NULL DEFAULT now(),
  student      text NOT NULL,
  status       text NOT NULL CHECK (status IN ('published','failed','ignored','duplicate')),
  subject_line text,
  sender       text,
  week_of      date,
  group_name   text,
  word_count   integer,
  doc_url      text,
  packet_id    uuid,
  detail       text,
  seen         boolean NOT NULL DEFAULT false
);
CREATE INDEX IF NOT EXISTS idx_intake_runs_recent ON intake_runs(student, created_at DESC);
ALTER TABLE intake_runs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS intake_runs_read ON intake_runs;
CREATE POLICY intake_runs_read ON intake_runs FOR SELECT TO anon, authenticated USING (true);
DROP POLICY IF EXISTS intake_runs_ack ON intake_runs;
CREATE POLICY intake_runs_ack ON intake_runs FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);
