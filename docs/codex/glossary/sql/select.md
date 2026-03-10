---
title: SELECT
id: glossary/sql/select
world: sql
level: beginner
tags: [queries, fundamentals, syntax]
related:
  - codex:glossary/sql/from
  - codex:glossary/sql/where
  - codex:glossary/sql/as
---

# SELECT

## Definition
The `SELECT` statement is the first part of almost every SQL query. It is used to specify exactly which **columns** or calculated values you want to retrieve from the database.

## Why It Matters
Data is often messy and vast. `SELECT` allows you to cut through the noise and only pull the specific information you need—such as just the "email" of a user instead of their entire record.

## Mental Model
Think of `SELECT` as a **filter for columns**. While other clauses filter which *rows* you see, `SELECT` determines which *fields* of those rows are visible in your final report.

## Example
```sql
-- Retrieve only the name and price for all products
SELECT name, price_cents
FROM products;
```

## Pitfalls
- **`SELECT *`**: While convenient, selecting everything can slow down your query and break your code if columns are added or removed from the table later. It is usually better to list your columns explicitly.
- **Missing Commas**: Forgetting a comma between column names is one of the most common syntax errors for beginners.

## Related
- FROM: Specifies the source table that SELECT pulls from.
- AS: Used to give the selected columns more readable names (aliasing).
