---
title: HAVING
id: glossary/world-sql/term-3
world: world-sql
level: intermediate
tags: [aggregation, filtering, grouping]
related:
  - codex:glossary/world-sql/term-1
  - codex:glossary/sql/where
  - codex:glossary/sql/select
  - codex:glossary/sql/order-by
---

# HAVING

## Definition
`HAVING` filters grouped results after aggregation. Use it when the condition depends on an aggregate like `COUNT(*)`, `SUM(x)`, etc.

## Usage
- **`WHERE`** filters rows before grouping.
- **`HAVING`** filters groups after grouping.
- Use HAVING for conditions on aggregates.

## Example
```sql
SELECT
  customer_id,
  COUNT(*) AS orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5
ORDER BY orders DESC;
```

## Pitfalls

* Writing aggregate filters in `WHERE` is invalid (use `HAVING`).
* Overusing `HAVING` for non-aggregate filters can be slower than filtering in `WHERE` first.

## Related

* GROUP BY: HAVING filters GROUP BY results.
* WHERE: WHERE filters rows; HAVING filters groups.
* SELECT: SELECT includes aggregates that HAVING filters.
* ORDER BY: ORDER BY can sort HAVING-filtered results.
