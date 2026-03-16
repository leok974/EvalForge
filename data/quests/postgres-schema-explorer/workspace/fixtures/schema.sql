CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    building TEXT
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    department_id INTEGER REFERENCES departments(id),
    salary NUMERIC(12, 2),
    hired_at TIMESTAMPTZ DEFAULT NOW(),
    skills TEXT[]
);

-- Enable pgvector for future use in this pack
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(3) -- Small vector for testing
);
