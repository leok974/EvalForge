---
id: glossary/sql/where
level: beginner
source: core
tags:
- fundamentals
- filtering
title: WHERE
world: sql
---

The `WHERE` clause is used to filter records. It ensures that only those rows that fulfill a specific condition are returned.

## Basic Comparison

```sql
SELECT * FROM users WHERE age >= 18;
```

## Logical Operators

You can combine multiple conditions using [AND](codex:glossary/sql/and) and **OR**.

```sql
SELECT * FROM users WHERE country = 'USA' AND is_active = 1;
```

## Special Operators

- **IN**: To match against a list of values.
- **LIKE**: To perform simple pattern matching (e.g., `%` for any characters).
- **BETWEEN**: To match within a range of values.
- **IS NULL**: To find [NULL](codex:glossary/sql/null) values.