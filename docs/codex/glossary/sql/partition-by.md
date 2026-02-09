---
title: PARTITION BY
id: glossary/sql/partition-by
world: sql
level: intermediate
tags: [window-functions, grouping, analytics]
related:
  - codex:glossary/sql/over
  - codex:glossary/sql/window-function
  - codex:glossary/sql/row-number
---

# PARTITION BY

## Definition
`PARTITION BY` divides rows into groups (partitions) for window functions, so calculations are performed independently within each group rather than across all rows.

## Usage
- Use inside `OVER (PARTITION BY column)` to group rows.
- Common for ranking, running totals, or comparisons within categories.
- Multiple columns can partition together.

## Example
```sql
SELECT
  user_id,
  created_at,
  amount,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS user_order_num
FROM orders;
```

## Pitfalls

* Partitioning by high-cardinality columns (like IDs) can create many tiny partitions.
* Forgetting `ORDER BY` inside `OVER` when needed for rankings.

## Related

* OVER: PARTITION BY is used inside OVER clauses.
* Window Function: PARTITION BY groups rows for window functions.
* ROW_NUMBER: ROW_NUMBER often uses PARTITION BY for per-group ranking.
