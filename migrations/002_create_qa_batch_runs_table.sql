-- Phase 8.1: Add batch run support
-- Creates qa_batch_runs table and links qa_runs to batches

-- 1. Add batch_id column to qa_runs (nullable for backwards compatibility)
ALTER TABLE qa_runs 
ADD COLUMN IF NOT EXISTS batch_id VARCHAR(64);

CREATE INDEX IF NOT EXISTS idx_qa_runs_batch ON qa_runs(batch_id);

-- 2. Create batch runs table
CREATE TABLE IF NOT EXISTS qa_batch_runs (
    id VARCHAR(64) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255) NOT NULL,  -- user_id
    
    -- Batch scope
    world_id VARCHAR(64),
    track_id VARCHAR(64),
    variant VARCHAR(32) NOT NULL DEFAULT 'integrity',
    
    -- Progress tracking
    status VARCHAR(32) NOT NULL DEFAULT 'queued',  -- queued, running, finished, failed
    total_quests INTEGER NOT NULL,
    completed_quests INTEGER NOT NULL DEFAULT 0,
    
    -- Results aggregation
    passed_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,
    
    -- Timing
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    duration_ms INTEGER,
    
    -- Metadata
    engine_version VARCHAR(64) DEFAULT 'phase-8.1'
);

-- 3. Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_batch_runs_created_by ON qa_batch_runs(created_by);
CREATE INDEX IF NOT EXISTS idx_batch_runs_status ON qa_batch_runs(status);
CREATE INDEX IF NOT EXISTS idx_batch_runs_world_track ON qa_batch_runs(world_id, track_id);
CREATE INDEX IF NOT EXISTS idx_batch_runs_created_at ON qa_batch_runs(created_at DESC);
