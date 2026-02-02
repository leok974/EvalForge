# FROM

## Definition
`FROM` defines the table (or source) the query reads rows from. Without `FROM`, many queries can’t access table data.

## Tiny example
```sql
SELECT id
FROM users;
```

## Common pitfall
Forgetting `FROM` or referencing the wrong table name leads to errors or empty results. When debugging, verify the table exists and contains rows.

## Related
SELECT, WHERE
