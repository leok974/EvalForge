---
title: ASC
id: glossary/sql/asc
world: sql
level: beginner
tags: [fundamentals, syntax, sorting]
related:
  - codex:glossary/sql/order-by
  - codex:glossary/sql/desc
---

# ASC

## Definition
The `ASC` keyword is used in an `ORDER BY` clause to sort data in **ascending order** (lowest to highest, A to Z).

## Why It Matters
`ASC` is the default sorting direction in SQL. Whether you're listing products alphabetically or sorting customers from oldest to newest, `ASC` ensures your output is predictable and organized.

## Core Syntax
```sql
SELECT ... FROM ...
ORDER BY column_name ASC;
```

## Example
```sql
-- List products sorted by price from cheapest to most expensive
SELECT name, price_cents
FROM products
ORDER BY price_cents ASC;
```

## Pitfalls
- **Default Behavior**: Since `ASC` is the default, you don't *have* to type it, but doing so can make your code clearer to others.
- **NULL Placement**: By default, `NULL` values usually appear at the top in ascending order, though this can vary by database type.

## Related
- ORDER BY: The clause that uses ASC for sorting.
- DESC: The opposite keyword used for descending (highest to lowest) order.
