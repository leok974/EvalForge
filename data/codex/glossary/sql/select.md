# SELECT

## Definition
`SELECT` chooses which columns (or expressions) to return in a query result. It defines the shape of each row in the output.

## Tiny example
```sql
SELECT id, name
FROM users;
```

## Common pitfall
Using `SELECT *` is convenient but often undesirable in real systems: it can return unnecessary columns and break when schemas change. Prefer selecting explicit columns.

## Related
FROM, WHERE
