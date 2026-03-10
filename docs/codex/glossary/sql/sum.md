---
title: SUM()
id: glossary/sql/sum
world: sql
level: beginner
tags: [fundamentals, aggregates]
related:
  - codex:glossary/sql/avg
  - codex:glossary/sql/count
---

# SUM()

## Definition
`SUM()` is an aggregate function that calculates the total addition of all numeric values in a specific column.

## Why It Matters
While `COUNT()` tells you "how many," `SUM()` tells you "how much." It is essential for financial reporting, inventory tracking, and any metric involving cumulative totals.

## Core Syntax
`SUM()` only works on numeric data types (integers, decimals, etc.). It ignores `NULL` values automatically.

## Example
```sql
-- Calculate the total revenue from all orders
SELECT SUM(total_cents) AS total_revenue_cents
FROM orders
WHERE status = 'paid';
```

## Pitfalls
- **Empty result sets**: If `SUM()` is run on a dataset with zero rows (or only `NULL` rows), it returns `NULL`, not `0`. You can use `COALESCE(SUM(col), 0)` to handle this.
- **Non-numeric columns**: Attempting to `SUM()` a text column will result in a database error.

## Related
- AVG: Calculates the mean instead of the total.
- COUNT: Returns the number of items instead of their total value.
