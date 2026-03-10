---
id: glossary/sql/from
level: beginner
source: core
tags:
- fundamentals
- query
title: FROM
world: sql
---

The `FROM` clause specifies the database table from which you want to retrieve data. It is used in combination with the [SELECT](codex:glossary/sql/select) statement.

## Usage

```sql
SELECT name FROM employees;
```

In this example, `employees` is the source table.

## Joining Tables

`FROM` is also where you define [JOIN](codex:glossary/sql/join) operations to combine data from multiple tables.

```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
```