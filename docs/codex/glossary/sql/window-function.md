---
title: Window Function
id: glossary/sql/window-function
world: sql
level: intermediate
tags: [analytics, advanced, functions]
related:
  - codex:glossary/sql/over
  - codex:glossary/sql/partition-by
  - codex:glossary/sql/row-number
---

# Window Function

## Definition
A **window function** performs calculations across a set of rows related to the current row, without collapsing groups (unlike `GROUP BY`). Common window functions include `ROW_NUMBER()`, `RANK()`, `SUM()`, `AVG()`, `LAG()`, and `LEAD()`.

## Usage
- Calculate running totals, moving averages, and rankings.
- Access previous/next rows with `LAG()`/`LEAD()`.
- Compare rows within partitions.

## Example
```sql
SELECT
  user_id,
  order_date,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS running_total,
  LAG(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS prev_amount
FROM orders;
```

## Pitfalls

* Window functions can't be used in `WHERE` (use subqueries instead).
* Forgetting `ORDER BY` inside `OVER` when order matters for the calculation.

## Related

* OVER: window functions use OVER to define windows.
* PARTITION BY: PARTITION BY groups rows for window calculations.
* ROW_NUMBER: ROW_NUMBER is a common window function.
