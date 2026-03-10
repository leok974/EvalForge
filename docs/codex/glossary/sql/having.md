---
id: glossary/sql/having
level: intermediate
source: core
tags:
- fundamentals
- aggregates
title: HAVING
world: sql
---

The `HAVING` clause was added to SQL because the [WHERE](codex:glossary/sql/where) keyword could not be used with aggregate functions.

## Difference between WHERE and HAVING

- `WHERE`: Filters rows **before** they are grouped.
- `HAVING`: Filters the groups themselves **after** grouping is performed.

## Usage

```sql
-- Find countries with more than 100 users
SELECT country, COUNT(*)
FROM users
GROUP BY country
HAVING COUNT(*) > 100;
```