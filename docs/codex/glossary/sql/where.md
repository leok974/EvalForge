---
title: WHERE
id: glossary/sql/where
world: sql
level: beginner
tags: [queries, filtering, conditions]
related:
  - codex:glossary/sql/from
  - codex:glossary/sql/select
  - codex:glossary/world-sql/term-3
---

# WHERE

## Definition
`WHERE` filters rows before grouping or aggregation. It limits the dataset early, which is usually good for performance and correctness.

## Usage
- Filter by equality, ranges, and patterns.
- Combine predicates with `AND` / `OR`.
- Use parentheses to control logic.

## Example
```sql
SELECT *
FROM transactions
WHERE amount > 100
  AND created_at >= '2026-01-01';
```

## Pitfalls

* `OR` conditions can be easy to misread—use parentheses.
* Filtering on a `LEFT JOIN` table in `WHERE` may turn it into an `INNER JOIN`.

## Related

* FROM: WHERE filters FROM results.
* SELECT: SELECT processes WHERE-filtered rows.
* HAVING: HAVING filters groups; WHERE filters rows (Term 3).
