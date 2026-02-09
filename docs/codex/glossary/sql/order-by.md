---
title: ORDER BY
id: glossary/sql/order-by
world: sql
level: beginner
tags: [queries, sorting, ordering]
related:
  - codex:glossary/sql/limit
  - codex:glossary/sql/select
  - codex:glossary/sql/where
---

# ORDER BY

## Definition
`ORDER BY` sorts the result set by one or more columns/expressions. Sorting is applied after filtering and grouping.

## Usage
- Use `ASC` (default) or `DESC`.
- You can order by aliases or column positions in some DBs, but aliases are clearer.
- Combine with LIMIT for "top N" queries.

## Example
```sql
SELECT id, created_at
FROM transactions
ORDER BY created_at DESC
LIMIT 20;
```

## Pitfalls

* Sorting large datasets is expensive—pair with `LIMIT` when appropriate.
* Ordering without a deterministic tie-breaker can produce unstable "top N" results.

## Related

* LIMIT: ORDER BY is often paired with LIMIT.
* SELECT: SELECT results are ordered by ORDER BY.
* WHERE: WHERE filters before ORDER BY sorts.
