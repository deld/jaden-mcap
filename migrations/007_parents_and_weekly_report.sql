-- Parents linked to students, and a log of the weekly progress email.
--
-- A student can have any number of parents; each parent row is one email
-- address that receives that student's weekly report. `student` is the same
-- text key the rest of the schema uses ('Jaden').
--
-- These rows hold email addresses, so - unlike most tables here - the anon
-- key gets NO access. The app's anon key is public; only the service role
-- (Edge Functions, the SQL editor) can read or change parents.
CREATE TABLE IF NOT EXISTS parents (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at      timestamptz NOT NULL DEFAULT now(),
  student         text NOT NULL,
  name            text,
  email           text NOT NULL,
  receives_report boolean NOT NULL DEFAULT true
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_parents_student_email ON parents(student, lower(email));
ALTER TABLE parents ENABLE ROW LEVEL SECURITY;  -- no policies: service role only

-- One row per student per week per attempt to send. A 'sent' row stops a
-- second firing of the schedule from emailing the same week twice.
CREATE TABLE IF NOT EXISTS report_runs (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at  timestamptz NOT NULL DEFAULT now(),
  student     text NOT NULL,
  week_of     date NOT NULL,
  status      text NOT NULL CHECK (status IN ('sent','failed')),
  recipients  integer NOT NULL DEFAULT 0,
  detail      text
);
CREATE INDEX IF NOT EXISTS idx_report_runs_week ON report_runs(student, week_of);
-- A failure detail can name a recipient's address, so this is service-role
-- only too.
ALTER TABLE report_runs ENABLE ROW LEVEL SECURITY;
