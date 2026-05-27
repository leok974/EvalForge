-- Sprint 10: Add tier column to questdefinition
-- Enables quest difficulty display (tier 1 = foundry, tier 2 = advanced, etc.)
-- Corresponds to Gap #4 from LEARNER_EXPERIENCE_GAPS.md

BEGIN;

ALTER TABLE questdefinition
  ADD COLUMN IF NOT EXISTS tier INTEGER NOT NULL DEFAULT 1;

-- Index for efficient tier-based filtering/sorting
CREATE INDEX IF NOT EXISTS idx_questdefinition_tier
  ON questdefinition (tier);

COMMIT;

-- Verification:
-- SELECT column_name, data_type, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'questdefinition' AND column_name = 'tier';
