-- Phase 8.x PR 3: Quest Idempotency Keys
-- Minimal migration: adds ONLY idempotency support
-- (workspace_hash, execution_context, model_id, prompt_version deferred to PR 4)

BEGIN;

-- Add idempotency_key column
ALTER TABLE quest_attempts
  ADD COLUMN IF NOT EXISTS idempotency_key TEXT;

-- Partial unique index: prevent duplicate submissions
-- Only enforced when idempotency_key IS NOT NULL
-- Uses existing is_submit column (boolean) to distinguish run vs submit
CREATE UNIQUE INDEX IF NOT EXISTS uq_quest_attempts_idempotency
  ON quest_attempts (user_id, quest_id, is_submit, idempotency_key)
  WHERE idempotency_key IS NOT NULL;

COMMIT;

-- Verification query (run after migration)
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'quest_attempts'
--   AND column_name = 'idempotency_key';
--
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'quest_attempts'
--   AND indexname = 'uq_quest_attempts_idempotency';
