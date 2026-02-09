---
title: ROW_NUMBER
id: glossary/sql/row-number
world: sql
level: intermediate
tags: [window-functions, ranking, analytics]
related:
  - codex:glossary/sql/over
  - codex:glossary/sql/partition-by
  - codex:glossary/sql/window-function
---

# ROW_NUMBER

## Definition
`ROW_NUMBER()` assigns a unique sequential number to each row within a partition, ordered by the specified columns. It's commonly used for ranking and pagination.

## Usage
- Use with `OVER (ORDER BY ...)` for global ranking.
- Use with `OVER (PARTITION BY ... ORDER BY ...)` for per-group ranking.
- Filter results with `WHERE row_num = 1` to get top rows per group.

## Example
```sql
SELECT *
FROM (
  SELECT
    user_id,
    order_id,
    created_at,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM orders
) ranked
WHERE rn = 1;  -- Most recent order per user
```

## Pitfalls

* `ROW_NUMBER()` is arbitrary for ties—use `RANK()` or `DENSE_RANK()` if order matters.
* Filtering `ROW_NUMBER()` requires a subquery (can't use it directly in `WHERE`).

## Related

* OVER: ROW_NUMBER uses OVER to define ordering.
* PARTITION BY: PARTITION BY groups rows for per-group numbering.
* Window Function: ROW_NUMBER is a window function.
