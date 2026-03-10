---
title: DESC
id: glossary/sql/desc
world: sql
level: beginner
tags: [fundamentals, syntax, sorting]
related:
  - codex:glossary/sql/order-by
  - codex:glossary/sql/asc
---

# DESC

## Definition
The `DESC` keyword is used in an `ORDER BY` clause to sort data in **descending order** (highest to lowest, Z to A).

## Why It Matters
`DESC` is essential whenever you want to see the "top" items first—such as the most recent orders, the highest-spending customers, or the most expensive products in your store.

## Core Syntax
```sql
SELECT ... FROM ...
ORDER BY column_name DESC;
```

## Example
```sql
-- Show the 5 most expensive products first
SELECT name, price_cents
FROM products
ORDER BY price_cents DESC
LIMIT 5;
```

## Pitfalls
- **Multi-column Sort**: If you are sorting by multiple columns (e.g., `ORDER BY city ASC, name DESC`), remember that each column needs its own direction keyword.
- **NULL Placement**: In descending order, `NULL` values usually appear at the bottom by default.

## Related
- ORDER BY: The clause that uses DESC for sorting.
- ASC: The opposite keyword used for ascending (lowest to highest) order.
