---
title: AVG()
id: glossary/sql/avg
world: sql
level: beginner
tags: [fundamentals, aggregates]
related:
  - codex:glossary/sql/sum
  - codex:glossary/sql/count
---

# AVG()

## Definition
`AVG()` is an aggregate function that calculates the mathematical mean (average) of all numeric values in a column.

## Why It Matters
`AVG()` is used to find central tendencies in your data. It answers questions like "What is the average order value?" or "What is the average age of our users?"

## Core Syntax
`AVG()` sums the values and divides them by the count of non-null rows. It automatically ignores `NULL` values in its calculation.

## Example
```sql
-- Find the average price of all products in the store
SELECT AVG(price_cents) AS average_product_price
FROM products;
```

## Pitfalls
- **Integer Division**: In some SQL dialects, averaging integers may truncate the result. It is often safer to multiply by `1.0` first: `AVG(price * 1.0)`.
- **NULL skew**: Since rows with `NULL` are excluded from the denominator, the average might be higher or lower than you expect if many values are missing.

## Related
- SUM: The total value used as the numerator for the average.
- COUNT: The number of items used as the denominator for the average.
