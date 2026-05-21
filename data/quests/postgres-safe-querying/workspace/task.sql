-- Quest: postgres-safe-querying
-- Goal: Inspect the employees table schema via information_schema,
--       then preview data safely with a row limit.

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
-- TODO: add WHERE clause to filter for table_name = 'employees'
-- TODO: add ORDER BY ordinal_position
-- TODO: add LIMIT 5
;
