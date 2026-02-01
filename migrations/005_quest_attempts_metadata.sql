-- Phase 8.x PR 4: Quest Workspace Hash + Metadata Persistence
-- Adds canonical workspace hashing + execution context tracking
-- (Complements PR 3 idempotency with replay debugging capabilities)

BEGIN;

-- Add metadata columns
ALTER TABLE quest_attempts
  ADD COLUMN IF NOT EXISTS workspace_hash TEXT,
  ADD COLUMN IF NOT EXISTS execution_context_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  ADD COLUMN IF NOT EXISTS model_id TEXT,
  ADD COLUMN IF NOT EXISTS prompt_version TEXT;

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_quest_attempts_quest_created
  ON quest_attempts (quest_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_quest_attempts_workspace_hash
  ON quest_attempts (workspace_hash);

CREATE INDEX IF NOT EXISTS idx_quest_attempts_model_id
  ON quest_attempts (model_id)
  WHERE model_id IS NOT NULL;

COMMIT;

-- Verification queries
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'quest_attempts'
--   AND column_name IN ('workspace_hash', 'execution_context_json', 'model_id', 'prompt_version')
-- ORDER BY column_name;
