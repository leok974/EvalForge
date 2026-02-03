---
title: HAVING
id: sql/having
---
# HAVING

Filters groups created by `GROUP BY`.

## Syntax
```sql
SELECT role, COUNT(*) FROM users GROUP BY role HAVING COUNT(*) > 5;
```

## WHERE vs HAVING
- `WHERE`: Filters rows (before grouping).
- `HAVING`: Filters groups (after grouping).
