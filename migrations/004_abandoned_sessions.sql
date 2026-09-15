-- A session is either completed by the timer or abandoned. There is no resume.
-- completed=true  -> the clock ran out (or the test was submitted)
-- abandoned=true  -> left early by any route; score/total hold what was answered
-- neither         -> still in progress (or a stale row that never got answers)
ALTER TABLE attempts
  ADD COLUMN IF NOT EXISTS abandoned       boolean NOT NULL DEFAULT false,
  ADD COLUMN IF NOT EXISTS planned_minutes integer;
CREATE INDEX IF NOT EXISTS idx_attempts_student_created ON attempts(student, created_at DESC);
