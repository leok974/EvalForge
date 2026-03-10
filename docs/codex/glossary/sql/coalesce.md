---
id: glossary/sql/coalesce
title: coalesce
world: sql
---

# coalesce

The `COALESCE()` function returns the first non-null value in a list of arguments. It is the primary tool for handling [NULL](glossary/sql/null) values in calculations and reports.

## Syntax

```sql
COALESCE(value1, value2, ..., valueN)
```

## Usage

Use `COALESCE` to provide a "fallback" or "default" value when a column might contain `NULL`.

```sql
-- Calculate total pay even if bonus is NULL
SELECT 
  name, 
  salary + COALESCE(bonus, 0) AS total_comp
FROM employees;
```

In the example above, if `bonus` is `NULL`, the `COALESCE` function returns `0`, preventing the entire calculation from becoming `NULL`.