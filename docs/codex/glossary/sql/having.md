---
title: HAVING
id: glossary/sql/having
world: sql
level: intermediate
tags: [fundamentals, aggregates, filtering]
related:
  - codex:glossary/sql/group-by
  - codex:glossary/sql/where
---

# HAVING

## Definition
The `HAVING` clause is used to filter the results created by a `GROUP BY` clause. It allows you to specify conditions that apply to the summarized aggregate values (like `COUNT`, `SUM`, etc.) rather than the individual rows.

## Why It Matters
`WHERE` cannot be used to filter on aggregate functions because it acts on individual rows *before* they are transformed into groups. `HAVING` acts on the groups *after* they have been calculated.

## Mental Model
- **`WHERE`**: Filters the raw ingredients.
- **`GROUP BY`**: Cooks the ingredients into groups.
- **`HAVING`**: Samples the cooked groups and decides which ones to keep.

## Example
```sql
-- Find cities that have more than 5 users
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
HAVING COUNT(*) > 5;
```

## Pitfalls
- **Using without Group By**: `HAVING` is almost always paired with `GROUP BY`. If used alone, it treats the entire table as a single group.
- **Performance**: Use `WHERE` as much as possible to reduce the data size *before* grouping, as `HAVING` happens later in the query execution.

## Related
- GROUP BY: The clause that defines the groups HAVING filters.
- WHERE: The row-level filter that happens before grouping.
