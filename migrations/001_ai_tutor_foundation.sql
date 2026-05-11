-- ============================================================
-- Migration: AI Tutor Foundation
-- Lays groundwork for multi-grade, multi-subject AI tutor
-- Run in Supabase SQL Editor: https://supabase.com/dashboard
-- ============================================================

-- ── 1. Extend questions ──────────────────────────────────────
ALTER TABLE questions
  ADD COLUMN IF NOT EXISTS grade  integer NOT NULL DEFAULT 3,
  ADD COLUMN IF NOT EXISTS source text    NOT NULL DEFAULT 'manual';
-- source: 'manual' | 'packet' | 'ai-generated'

-- Tag all existing questions as Grade 3, manual
UPDATE questions SET grade = 3, source = 'manual'
  WHERE grade IS NULL OR source IS NULL;

CREATE INDEX IF NOT EXISTS idx_questions_grade  ON questions(grade);
CREATE INDEX IF NOT EXISTS idx_questions_source ON questions(source);

-- ── 2. Extend lesson_map ─────────────────────────────────────
ALTER TABLE lesson_map
  ADD COLUMN IF NOT EXISTS grade   integer NOT NULL DEFAULT 3,
  ADD COLUMN IF NOT EXISTS subject text    NOT NULL DEFAULT 'Math';

-- ── 3. student_grade in app_config ──────────────────────────
INSERT INTO app_config (key, value)
  VALUES ('student_grade', '3')
  ON CONFLICT (key) DO NOTHING;

-- ── 4. topics table (curriculum map: Grade > Subject > Unit > Skill)
CREATE TABLE IF NOT EXISTS topics (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  grade       integer     NOT NULL,
  subject     text        NOT NULL,
  unit        text        NOT NULL,
  skill       text        NOT NULL,
  description text,
  active      boolean     NOT NULL DEFAULT true,
  created_at  timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE topics ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon read topics" ON topics;
CREATE POLICY "anon read topics" ON topics FOR SELECT TO anon USING (true);

CREATE INDEX IF NOT EXISTS idx_topics_grade_subj ON topics(grade, subject);

-- ── 5. packets (weekly homework uploads) ─────────────────────
CREATE TABLE IF NOT EXISTS packets (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  student       text        NOT NULL DEFAULT 'Jaden',
  grade         integer     NOT NULL DEFAULT 3,
  subject       text        NOT NULL,
  week_of       date,
  raw_image_url text,
  status        text        NOT NULL DEFAULT 'pending',
  -- status: 'pending' | 'processed' | 'approved'
  notes         text,
  created_at    timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE packets ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon manage packets" ON packets;
CREATE POLICY "anon manage packets" ON packets FOR ALL TO anon
  USING (true) WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_packets_student ON packets(student);

-- ── 6. packet_questions (extracted questions awaiting approval)
CREATE TABLE IF NOT EXISTS packet_questions (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  packet_id   uuid        REFERENCES packets(id) ON DELETE CASCADE,
  raw_text    text,
  structured  jsonb,      -- matches questions schema when parsed
  approved    boolean     DEFAULT false,
  question_id uuid        REFERENCES questions(id) ON DELETE SET NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE packet_questions ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon manage packet_questions" ON packet_questions;
CREATE POLICY "anon manage packet_questions" ON packet_questions FOR ALL TO anon
  USING (true) WITH CHECK (true);
