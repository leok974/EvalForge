---
title: LIMIT & OFFSET
id: sql/limit-offset
---
# LIMIT & OFFSET

Constrains the number of rows returned.

## Syntax
```sql
SELECT * FROM users LIMIT 10 OFFSET 5;
```

## Use Case
- Pagination (page 2 of 10 items per page).

## Gotchas
- Always use with `ORDER BY` for deterministic results.
