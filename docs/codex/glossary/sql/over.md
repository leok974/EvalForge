---
title: OVER
id: glossary/sql/over
world: sql
level: intermediate
tags: [window-functions, analytics, advanced]
related:
  - codex:glossary/sql/window-function
  - codex:glossary/sql/partition-by
  - codex:glossary/sql/row-number
---

# OVER

## Definition
`OVER` defines a window for window functions, specifying how rows are grouped and ordered for calculations that span multiple rows (like running totals, rankings, and moving averages).

## Usage
- Use `OVER ()` for calculations over all rows.
- Use `OVER (PARTITION BY ...)` to group rows.
- Use `OVER (ORDER BY ...)` for ranked or cumulative calculations.

## Example
```sql
SELECT
  id,
  amount,
  SUM(amount) OVER (ORDER BY created_at) AS running_total
FROM transactions;
```

## Pitfalls

* Empty `OVER ()` applies to all rows—can be expensive on large tables.
* Order matters: `ORDER BY` inside `OVER` affects ranking/cumulative calculations.

## Related

* Window Function: OVER is used with window functions.
* PARTITION BY: PARTITION BY groups rows within OVER.
* ROW_NUMBER: ROW_NUMBER uses OVER for ranking.
