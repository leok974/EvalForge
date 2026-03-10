---
title: FROM
id: glossary/sql/from
world: sql
level: beginner
tags: [queries, fundamentals, tables]
related:
  - codex:glossary/sql/select
  - codex:glossary/sql/join
---

# FROM

## Definition
The `FROM` clause identifies the **source table** or tables that you want to pull data from. It tells the database exactly where the columns you listed in the `SELECT` clause are located.

## Why It Matters
Without `FROM`, the database doesn't know which dataset you are talking about. It is the starting point for almost every query, defining the "universe" of data you are currently exploring.

## Mental Model
If a database is a library, the `FROM` clause is like picking a specific **book** (table) off the shelf. Everything else in your query refers to the pages and information *inside* that specific book.

## Example
```sql
-- Open the users table to retrieve all email addresses
SELECT email
FROM users;
```

## Pitfalls
- **Misspelled Table Names**: If you misspell the table name, the query will fail. Always double-check your schema (e.g., `user` vs. `users`).
- **Missing Join Logic**: If you pull from multiple tables without a `JOIN` or `WHERE` clause to link them, you will get a "Cartesian product," matching every row in Table A with every row in Table B.

## Related
- SELECT: The clause that pulls columns from the table specified in FROM.
- JOIN: Used within the FROM context to combine multiple tables.
