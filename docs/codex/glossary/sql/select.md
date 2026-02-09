---
title: SELECT
id: glossary/sql/select
world: sql
level: beginner
tags: [queries, fundamentals, syntax]
related:
  - codex:glossary/sql/from
  - codex:glossary/sql/where
  - codex:glossary/sql/order-by
  - codex:glossary/sql/limit
---

# SELECT

## Definition
`SELECT` chooses which columns/expressions to return from a query. It can return raw columns, computed expressions, and aggregated values.

## Usage
- Return specific columns instead of `*`.
- Alias computed columns with `AS`.
- Combine with `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`.

## Example
```sql
SELECT
  id,
  amount,
  amount * 1.07 AS amount_with_tax
FROM transactions
LIMIT 10;
```

## Pitfalls

* `SELECT *` can be fragile when schemas change.
* Aliases may not be available in `WHERE` (depends on DB); use a subquery/CTE if needed.

## Related

* FROM: SELECT pulls data from tables specified in FROM.
* WHERE: WHERE filters rows before SELECT processes them.
* ORDER BY: SELECT results can be ordered.
* LIMIT: LIMIT restricts SELECT output.
