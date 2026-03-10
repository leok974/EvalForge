---
title: UPDATE
id: glossary/sql/update
world: sql
level: intermediate
tags: [fundamentals, mutation, syntax]
related:
  - codex:glossary/sql/insert
  - codex:glossary/sql/delete
  - codex:glossary/sql/where
---

# UPDATE

## Definition
The `UPDATE` statement is used to modify existing records in a table. It allows you to change the values of one or more columns for rows that meet a specific condition.

## Why It Matters
Data is rarely static. Users change their emails, product prices are adjusted, and order statuses move from "pending" to "shipped." `UPDATE` keeps your data accurate over time.

## Core Syntax
```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

## Example
```sql
-- Mark a product as discontinued and drop its price
UPDATE products
SET is_discontinued = 1, price_cents = 2900
WHERE id = 4;
```

## Pitfalls
- **Missing WHERE Clause**: If you forget the `WHERE` clause, **every single row** in the table will be updated. This is one of the most common and dangerous SQL mistakes.
- **Data Truncation**: Trying to update a column with a value that exceeds its allowed length (if defined) will cause an error.

## Related
- WHERE: Crucial for limiting the scope of an update.
- INSERT: Used for adding new data rather than changing old data.
