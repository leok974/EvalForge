CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
