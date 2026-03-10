---
title: ORDER BY
id: glossary/sql/order-by
world: sql
level: beginner
tags: [queries, fundamentals, sorting]
related:
  - codex:glossary/sql/asc
  - codex:glossary/sql/desc
  - codex:glossary/sql/limit
---

# ORDER BY

## Definition
The `ORDER BY` clause is used to **sort** your result set in either ascending or descending order. Without it, the order in which rows are returned is not guaranteed.

## Why It Matters
Sorted data is much easier for humans to read and understand. Whether you want to see your highest-paying customers at the top of a list or organize products alphabetically, `ORDER BY` is the tool for the job.

## Core Syntax
```sql
SELECT ... FROM ...
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC];
```
- **ASC**: Ascending (default).
- **DESC**: Descending.

## Example
```sql
-- Sort users by city (A-Z) and then by age (oldest first)
SELECT name, city, age
FROM users
ORDER BY city ASC, age DESC;
```

## Pitfalls
- **Impact on Performance**: Sorting thousands or millions of rows can be slow. Ensure your database has "Indexes" on columns that you sort by frequently.
- **Nondeterministic Sort**: If you sort by a column with many identical values (like `city`) and don't provide a second sort key (like `id`), the order of rows within each city might change every time you run the query.

## Related
- ASC: The keyword for ascending order.
- DESC: The keyword for descending order.
- LIMIT: Often used after sorting to get the "Top N" results.
