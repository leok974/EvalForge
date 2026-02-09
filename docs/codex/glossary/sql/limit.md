---
title: LIMIT
id: glossary/sql/limit
world: sql
level: beginner
tags: [queries, pagination, performance]
related:
  - codex:glossary/sql/order-by
  - codex:glossary/sql/where
---

# LIMIT

## Definition
`LIMIT` restricts how many rows are returned. It's often used for previews and pagination.

## Usage
- Commonly paired with `ORDER BY` to get the "top N" newest/highest values.
- Use for previewing large result sets.
- Combine with OFFSET for pagination (though keyset pagination is better for large tables).

## Example
```sql
SELECT *
FROM logs
ORDER BY created_at DESC
LIMIT 50;
```

## Pitfalls

* `LIMIT` without `ORDER BY` is nondeterministic.
* Pagination with `OFFSET` can get slow; prefer keyset pagination for big tables.

## Related

* ORDER BY: LIMIT is usually paired with ORDER BY.
* WHERE: WHERE filters before LIMIT restricts.
