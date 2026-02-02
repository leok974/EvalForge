# ORDER BY

## Definition
`ORDER BY` sorts the returned rows by one or more columns. Sorting happens after filtering and selection.

## Tiny example
```sql
SELECT id, created_at
FROM users
ORDER BY created_at DESC;
```

## Common pitfall
Assuming results are “naturally ordered.” Without `ORDER BY`, the database can return rows in any order. Always specify ordering when order matters.

## Related
LIMIT, Window Functions
