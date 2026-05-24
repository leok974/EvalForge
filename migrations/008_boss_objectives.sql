-- Sprint 19: Boss deterministic objectives
-- Adds objectives_json to bossdefinition so boss quests can define structural
-- checks (yaml_structure, source_regex, etc.) that gate the LLM rubric.
-- Also restores technical_objective (was commented out in models.py) used
-- by the boss prompt and the /api/boss/current response.

BEGIN;

ALTER TABLE bossdefinition
  ADD COLUMN IF NOT EXISTS objectives_json JSONB NOT NULL DEFAULT '[]',
  ADD COLUMN IF NOT EXISTS technical_objective VARCHAR(500) NOT NULL DEFAULT '';

COMMIT;

-- Verification:
-- SELECT column_name, data_type, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'bossdefinition'
-- AND column_name IN ('objectives_json', 'technical_objective');
