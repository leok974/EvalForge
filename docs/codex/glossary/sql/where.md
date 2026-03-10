---
title: WHERE
id: glossary/sql/where
world: sql
level: beginner
tags: [queries, filtering, conditions]
related:
  - codex:glossary/sql/and
  - codex:glossary/sql/null
  - codex:glossary/sql/select
---

# WHERE

## Definition
The `WHERE` clause is used to **filter rows** based on a specific condition. It ensures that the database only returns the records that meet your criteria.

## Why It Matters
Most databases contain millions of rows, but you usually only care about a few. `WHERE` allows you to zoom in on specific data, such as "users who live in Seattle" or "orders over $100."

## Mental Model
Think of `WHERE` as a **gatekeeper for rows**. It inspects every row in the table and only allows those that pass its "test" to move forward to the final result set.

## Example
```sql
-- Filter for products that are currently discontinued
SELECT name, price_cents
FROM products
WHERE is_discontinued = 1;
```

## Pitfalls
- **Quotes on Strings**: In SQL, text values (strings) **must** be surrounded by single quotes (e.g., `'Seattle'`), while numbers are not.
- **NULL Comparisons**: You cannot use `=` to check for `NULL`. You must use the special `IS NULL` or `IS NOT NULL` operators.

## Related
- AND: Used to combine multiple conditions in a single WHERE clause.
- SELECT: Retrieves columns from the rows that pass the WHERE filter.
