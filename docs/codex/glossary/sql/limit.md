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
The `LIMIT` clause specifies the **maximum number of rows** that the database should return. It "caps" the output at a certain count.

## Why It Matters
If a table has a million rows, trying to see all of them at once will crash your browser or slow down your computer. `LIMIT` allows you to safely preview data or create "Top 10" lists.

## Mental Model
Think of `LIMIT` as a **safety valve** at the very end of your query pipe. No matter how much data passed through the filters earlier, only the first few rows are allowed to exit the pipe.

## Example
```sql
-- Get a quick preview of the first 5 records in the orders table
SELECT * 
FROM orders 
LIMIT 5;
```

## Pitfalls
- **Unpredictable Results**: `LIMIT` is almost useless without an `ORDER BY` clause. Without sorting, `LIMIT 1` will give you a "random" row from the table every time.
- **Placement**: `LIMIT` must always be the very last clause in your query (except for potentially an `OFFSET`).

## Related
- ORDER BY: Used to ensure the rows capped by LIMIT are the ones you actually wanted (e.g., the newest or most expensive).
- WHERE: Filters the data *before* the LIMIT is applied.
