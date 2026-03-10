---
title: COUNT()
id: glossary/sql/count
world: sql
level: beginner
tags: [fundamentals, aggregates]
related:
  - codex:glossary/sql/sum
  - codex:glossary/sql/group-by
---

# COUNT()

## Definition
`COUNT()` is an aggregate function that returns the number of rows that match a specific criterion. It is one of the most frequently used functions for data analysis and reporting.

## Why It Matters
`COUNT()` allows you to answer volume-based questions: "How many users are registered?", "How many orders were placed today?", or "How many products are in the electronics category?"

## Core Syntax
- **`COUNT(*)`**: Counts every row in the result set, including those with `NULL` values.
- **`COUNT(column_name)`**: Counts only the rows where the specified column is **not** `NULL`.
- **`COUNT(DISTINCT column_name)`**: Counts only the unique, non-null values in a column.

## Example
```sql
-- Count total number of active users
SELECT COUNT(*) AS active_user_count
FROM users
WHERE is_active = 1;
```

## Pitfalls
- **NULL Handling**: Remember that `COUNT(email)` will skip users without an email address, whereas `COUNT(*)` will include them.
- **Missing GROUP BY**: If you use `COUNT()` alongside a non-aggregated column (like `city`), you **must** use a `GROUP BY` clause.

## Related
- SUM: Adds up numeric values instead of counting rows.
- GROUP BY: Used to get counts per category or group.
