# WHERE

## Definition
`WHERE` filters rows based on conditions. Only rows where the condition evaluates to true are returned.

## Tiny example
```sql
SELECT id, name
FROM users
WHERE active = true;
```

## Common pitfall
Be careful with `NULL`. Comparisons like `= NULL` don’t work as you expect. Use `IS NULL` / `IS NOT NULL` for null checks.

## Related
SELECT, ORDER BY
