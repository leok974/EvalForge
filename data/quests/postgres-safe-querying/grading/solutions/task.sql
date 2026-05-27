SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'employees'
ORDER BY ordinal_position
LIMIT 5;
