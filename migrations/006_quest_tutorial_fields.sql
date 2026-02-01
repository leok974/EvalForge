-- Phase 9.1: Quest Tutorial System - Schema
-- Adds tutorial fields to questdefinition table
-- All fields optional initially (Phase A: no breaking changes)

BEGIN;

-- Add tutorial fields
ALTER TABLE questdefinition
  ADD COLUMN IF NOT EXISTS tutorial_md TEXT,
  ADD COLUMN IF NOT EXISTS key_terms JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS concept_tags JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS codex_references JSONB DEFAULT '[]'::jsonb;

-- Index for efficient concept tag searches
CREATE INDEX IF NOT EXISTS idx_questdefinition_concept_tags
  ON questdefinition USING GIN (concept_tags);

-- Index for key terms searches
CREATE INDEX IF NOT EXISTS idx_questdefinition_key_terms
  ON questdefinition USING GIN (key_terms);

COMMIT;

-- Verification queries
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'questdefinition'
--   AND column_name IN ('tutorial_md', 'key_terms', 'concept_tags', 'codex_references')
-- ORDER BY column_name;
--
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'questdefinition'
--   AND indexname LIKE '%concept%' OR indexname LIKE '%key_terms%';
