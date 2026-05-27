## Hint 1
Query `information_schema.columns` — it is a built-in PostgreSQL view. You do not need to create it.

## Hint 2
Add `WHERE table_name = 'employees'` to limit results to the employees table only.

## Hint 3
Add `ORDER BY ordinal_position` to return columns in the order they were defined, then `LIMIT 5` at the end.
