---
title: NULLs
id: sql/nulls
---
# NULLs

Represents missing or unknown data.

## Checking for NULL
```sql
SELECT * FROM users WHERE email IS NULL;
```
(Do not use `= NULL`)

## Functions
- `COALESCE(val, default)`: Returns first non-null value.
