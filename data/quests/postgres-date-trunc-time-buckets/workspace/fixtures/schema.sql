CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    temperature NUMERIC(5, 2),
    recorded_at TIMESTAMPTZ NOT NULL
);
