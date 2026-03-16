---
id: world-sql/seq-scan
title: Sequential Scan
world: sql
---

# Sequential Scan (Seq Scan)

A **Sequential Scan** occurs when the database reads every single row in a table from start to finish to find the rows that match your query. 

## When it happens
- **No suitable index exists**: The database has no fast-lookup structure for your `WHERE` clause.
- **Small tables**: For very small tables, it's faster to just read the whole table into memory than to traverse an index.
- **Large result sets**: If your query requests a large percentage of the table, the database determines it's more efficient to read sequentially rather than doing random index lookups.

## Performance Impact
As tables grow larger, a Sequential Scan becomes progressively slower and more expensive, often leading to performance bottlenecks. In a PostgreSQL execution plan, it appears as:

```text
->  Seq Scan on large_table
      Filter: (status = 'pending')
```
