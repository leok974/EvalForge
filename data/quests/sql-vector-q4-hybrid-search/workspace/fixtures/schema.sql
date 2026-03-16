-- Archive Fragments Schema
CREATE TABLE IF NOT EXISTS historical_fragments (
    fragment_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    category TEXT,
    embedding VECTOR(3)
);
