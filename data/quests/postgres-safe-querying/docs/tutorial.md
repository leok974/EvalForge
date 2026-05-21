# Safe Database Exploration in PostgreSQL

## information_schema

PostgreSQL ships with a system catalog called `information_schema` that describes the database itself. The `information_schema.columns` view lets you query column metadata without touching the actual table data.

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;
```

Key columns:
- `column_name` — the name of the column
- `data_type` — e.g. `text`, `integer`, `timestamp with time zone`
- `is_nullable` — `YES` or `NO`
- `ordinal_position` — the column's position in the table definition

## LIMIT for safe previews

Always use LIMIT before running a query on an unknown or large table:

```sql
SELECT * FROM large_table LIMIT 10;
```

LIMIT prevents accidental full-table scans that could lock resources or return millions of rows. In production, never SELECT without a limit when exploring unfamiliar data.

## Combining both

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'my_table'
ORDER BY ordinal_position
LIMIT 5;
```

This lets you quickly understand a table's structure before writing any business queries.
