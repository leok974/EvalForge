---
id: world-sql/index-scan
title: Index Scan
world: sql
---

# Index Scan

When executing a query, an **Index Scan** means the database uses an [index](glossary/sql/index) structure (like a B-Tree) to quickly find specific rows matching your filter criteria, rather than reading the entire table.

## Why it matters
- **Speed**: Index scans are generally much faster than Sequential Scans for queries that return a small percentage of the table's rows.
- **Efficiency**: They reduce the amount of disk I/O and memory the database requires.

## Example in EXPLAIN
In a PostgreSQL execution plan, it appears as:
```text
->  Index Scan using users_email_idx on users
      Index Cond: (email = 'alice@example.com'::text)
```
