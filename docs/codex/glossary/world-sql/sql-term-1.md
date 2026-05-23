---
title: GROUP BY
id: glossary/world-sql/term-1
world: world-sql
level: intermediate
tags: [aggregation, grouping, analytics]
related:
  - codex:glossary/sql/select
  - codex:glossary/sql/from
  - codex:glossary/sql/where
  - codex:glossary/sql/order-by
  - codex:glossary/sql/limit
---

# GROUP BY

## Definition
`GROUP BY` aggregates rows into groups so you can compute summaries like counts, sums, and averages per group. It's used with aggregate functions such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`.

## Usage
- Use `GROUP BY` when you want one result row per group (e.g., per customer, per category).
- Any selected column that is not aggregated must appear in the `GROUP BY` clause.
- Combine with aggregate functions in SELECT.

## Example
```sql
SELECT
  customer_id,
  COUNT(*) AS orders,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY customer_id
ORDER BY revenue DESC;
```

## Pitfalls

* Selecting non-aggregated columns that aren't in `GROUP BY` is invalid (or nondeterministic in some DBs).
* `WHERE` filters before grouping; use `HAVING` to filter after grouping.

## Related

* SELECT: SELECT includes aggregates and GROUP BY columns.
* FROM: GROUP BY groups rows from FROM tables.
* WHERE: WHERE filters before GROUP BY groups.
* ORDER BY: ORDER BY can sort grouped results.
* LIMIT: LIMIT restricts grouped output.
