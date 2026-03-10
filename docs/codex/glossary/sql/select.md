---
id: glossary/sql/select
level: beginner
source: core
tags:
- fundamentals
- query
title: SELECT
world: sql
---

The `SELECT` statement is the most fundamental command in SQL. It is used to retrieve data from one or more tables.

## Basic Syntax

```sql
SELECT column1, column2 FROM table_name;
```

## Selecting All Columns

To select every column in a table, use the asterisk (`*`) wildcard:

```sql
SELECT * FROM users;
```

## Unique Values

Use the `DISTINCT` keyword to return only unique values, suppressing duplicates:

```sql
SELECT DISTINCT country FROM users;
```