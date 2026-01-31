-- Migration: Create QA Runs Table for Quest Health Dashboard
-- Phase: 8.0
-- Date: 2026-01-31

CREATE TABLE IF NOT EXISTS qa_runs (
    id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    quest_slug VARCHAR NOT NULL,
    variant VARCHAR NOT NULL,
    
    status VARCHAR NOT NULL DEFAULT 'queued',
    duration_ms INTEGER,
    
    result_json JSONB NOT NULL DEFAULT '{}',
    logs_sanitized TEXT,
    diagnostics_json JSONB NOT NULL DEFAULT '{}',
    test_summary_json JSONB NOT NULL DEFAULT '{}',
    
    engine_version VARCHAR,
    content_hash VARCHAR
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_qa_runs_quest_slug ON qa_runs(quest_slug);
CREATE INDEX IF NOT EXISTS idx_qa_runs_created_at ON qa_runs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_qa_runs_status ON qa_runs(status);
CREATE INDEX IF NOT EXISTS idx_qa_runs_variant ON qa_runs(variant);

-- Composite index for "latest run per quest" query
CREATE INDEX IF NOT EXISTS idx_qa_runs_quest_created ON qa_runs(quest_slug, created_at DESC);
