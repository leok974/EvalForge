---
id: world-sql/explain
title: EXPLAIN
world: sql
---

# EXPLAIN

The `EXPLAIN` command is used to see the internal strategy the database engine uses to execute a query. It is the primary tool for performance profiling in SQL.

## Usage

Prefix any `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement with the command:

### PostgreSQL
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users WHERE email = 'alice@example.com';
```
*(Note: Use `ANALYZE` to execute the query and see real timings, but use caution with destructive statements.)*

### SQLite
```sql
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'alice@example.com';
```

## Plan Cost

In PostgreSQL, `cost` is an estimate of how much work is required. Lower numbers are better.
