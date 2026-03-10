---
id: glossary/sql/group-by
level: intermediate
source: core
tags:
- fundamentals
- aggregates
title: GROUP BY
world: sql
---

The `GROUP BY` clause groups rows that have the same values into summary rows, like "find the number of customers in each country".

## Usage with Aggregates

`GROUP BY` is almost always used with aggregate functions like `COUNT()`, `MAX()`, `MIN()`, `SUM()`, or `AVG()`.

```sql
-- Count users per country
SELECT country, COUNT(*) 
FROM users 
GROUP BY country;
```

## Rules

Any column in your `SELECT` list that is not part of an aggregate function **must** be included in the `GROUP BY` clause.