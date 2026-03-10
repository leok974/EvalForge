---
id: glossary/sql/alias
title: alias
world: sql
---

# alias

An **alias** is a temporary name given to a table or a column in a query. It is created using the `AS` keyword and is used to make column headers more readable or to distinguish between tables in a join.

## Usage: Column Alias

```sql
-- Rename a calculated column
SELECT salary * 12 AS annual_salary FROM employees;
```

## Usage: Table Alias

```sql
-- Use short names (e, m) for easier typing
SELECT e.name, m.name as manager_name
FROM employees e
JOIN employees m ON e.manager_id = m.id;
```

Aliases only exist for the duration of the query.