---
title: AS (Aliasing)
id: glossary/sql/as
world: sql
level: beginner
tags: [fundamentals, syntax, readability]
related:
  - codex:glossary/sql/select
  - codex:glossary/sql/from
---

# AS (Aliasing)

## Definition
The `AS` keyword is used to give a table or a column a **temporary name** (alias). This name only exists for the duration of the query.

## Why It Matters
Aliases make your query results cleaner and your SQL code easier to read. They are especially useful for naming calculated columns (like `price * 0.1`) or giving short names to long table names during a join.

## Syntax
- **Column Alias**: `SELECT column_name AS alias_name ...`
- **Table Alias**: `SELECT ... FROM table_name AS alias_name`

## Example
```sql
-- Use an alias for a calculated column and a short name for the table
SELECT 
  p.name, 
  p.price_cents / 100.0 AS price_dollars
FROM products AS p;
```

## Pitfalls
- **Spaces in Names**: If your alias name has spaces (e.g., `AS "Total Price"`), you must surround it with double quotes.
- **Scope**: You cannot use a column alias inside a `WHERE` clause in many SQL dialects; you must use the original column name instead.

## Related
- SELECT: The most common place to use column aliases.
- FROM: Table aliases are often defined here to simplify joins.
