---
title: GROUP BY
id: sql/group-by
---
# GROUP BY

Groups rows that have the same values into summary rows.

## Syntax
```sql
SELECT role, COUNT(*) FROM users GROUP BY role;
```

## Gotchas
- Every non-aggregated column in SELECT must be in GROUP BY.
