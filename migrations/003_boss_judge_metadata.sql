-- Phase 8.x: Boss Judge Tighten Pack
-- Adds metadata fields for fail-closed judge validation

-- Add boss judge metadata columns to bossrun
ALTER TABLE bossrun
ADD COLUMN IF NOT EXISTS judge_model_id VARCHAR(128),
ADD COLUMN IF NOT EXISTS judge_prompt_version VARCHAR(64),
ADD COLUMN IF NOT EXISTS judge_schema_valid BOOLEAN,
ADD COLUMN IF NOT EXISTS judge_error_code VARCHAR(64),
ADD COLUMN IF NOT EXISTS judge_raw_response_trunc TEXT,
ADD COLUMN IF NOT EXISTS judge_result_json JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS submission_hash VARCHAR(128);

-- Indexes for debugging and analytics
CREATE INDEX IF NOT EXISTS idx_bossrun_judge_error ON bossrun(judge_error_code) WHERE judge_error_code IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_bossrun_schema_valid ON bossrun(judge_schema_valid);
CREATE INDEX IF NOT EXISTS idx_bossrun_judge_model ON bossrun(judge_model_id);
CREATE INDEX IF NOT EXISTS idx_bossrun_submission_hash ON bossrun(submission_hash);

-- Performance: index on completed_at for recent runs queries
CREATE INDEX IF NOT EXISTS idx_bossrun_completed_at ON bossrun(completed_at DESC);
