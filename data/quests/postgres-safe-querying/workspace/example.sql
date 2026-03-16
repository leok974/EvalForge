-- Example: Listing all tables in the current schema
-- A safe way to see what's available before querying.

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
