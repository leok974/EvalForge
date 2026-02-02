# LIMIT

## Definition
`LIMIT` restricts the number of rows returned. It’s useful for debugging and for “top N” queries.

## Tiny example
```sql
SELECT *
FROM users
ORDER BY created_at DESC
LIMIT 10;
```

## Common pitfall
If you use `LIMIT` without `ORDER BY`, the “top” rows are arbitrary. For meaningful “top N,” always sort first.

## Related
ORDER BY, SELECT
