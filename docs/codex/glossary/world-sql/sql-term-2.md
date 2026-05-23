---
title: JOIN
id: glossary/world-sql/term-2
world: world-sql
level: intermediate
tags: [queries, relationships, tables]
related:
  - codex:glossary/sql/from
  - codex:glossary/sql/where
  - codex:glossary/sql/select
  - codex:glossary/world-sql/term-1
---

# JOIN

## Definition
A `JOIN` combines rows from two tables using a matching condition (usually keys). Joins let you model relationships like "transactions belong to users" or "orders have line items."

## Usage
- **`INNER JOIN`**: only matching rows.
- **`LEFT JOIN`**: all rows from left table, matches from right (or NULLs).
- **`RIGHT JOIN`**: all rows from right table (less common).
- **`FULL OUTER JOIN`**: all rows from both sides (or NULLs).

## Example
```sql
SELECT
  o.id,
  o.created_at,
  u.email
FROM orders o
JOIN users u
  ON u.id = o.user_id
WHERE o.created_at >= '2026-01-01'
ORDER BY o.created_at DESC;
```

## Pitfalls

* Joining on the wrong key can silently multiply rows (cartesian-like blowups).
* Filtering on the right table in `WHERE` can turn a `LEFT JOIN` into an implicit `INNER JOIN`.

## Related

* FROM: joins are specified in the FROM clause.
* WHERE: WHERE filters joined results.
* SELECT: SELECT pulls columns from joined tables.
* GROUP BY: GROUP BY can aggregate joined data.
