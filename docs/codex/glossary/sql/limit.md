---
id: glossary/sql/limit
level: beginner
source: core
tags:
- fundamentals
- pagination
title: LIMIT
world: sql
---

The `LIMIT` clause is used to specify the maximum number of records to return. It is extremely useful for performance on large tables or for creating pagination.

## Usage

```sql
-- Get the 5 most recent users
SELECT * FROM users ORDER BY created_at DESC LIMIT 5;
```

## Offset

You can use `OFFSET` to skip a specified number of rows before beginning to return results.

```sql
-- Skip the first 10, then get 10
SELECT * FROM users LIMIT 10 OFFSET 10;
```