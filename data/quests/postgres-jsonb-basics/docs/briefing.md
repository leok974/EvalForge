# PostgreSQL: JSONB Basics

Your event ingestion pipeline stores raw webhook payloads as JSONB in the `webhook_events` table. An analyst needs to report on active events: which user triggered them and what action was taken.

Your task: use the PostgreSQL JSONB `->>` operator to extract `user_id` and `action` as text fields from the `payload` column, and filter the results to only include events where `payload->>'status' = 'active'`.
