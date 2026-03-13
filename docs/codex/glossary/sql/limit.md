---
id: glossary/sql/limit
title: LIMIT
world: sql
---

# LIMIT

The `LIMIT` clause is used to specify the maximum number of rows that the database should return in a query result. This is essential for preventing large datasets from overwhelming your application or the database server.

## Basic Syntax

```sql
SELECT column1, column2 FROM table_name LIMIT number;
```

## Why use LIMIT?

1. **Performance**: Stops the database engine as soon as the quota is met.
2. **Safety**: Prevents crashing your IDE or browser when querying massive tables.
3. **Paging**: Often used with `OFFSET` to implement pagination in applications.

## Example

Inspect the first 5 records of an unknown table:
```sql
SELECT * FROM massive_production_table LIMIT 5;
```