---
id: glossary/sql/order-by
level: beginner
source: core
tags:
- fundamentals
- sorting
title: ORDER BY
world: sql
---

The `ORDER BY` clause is used to sort the result set in either [ascending](codex:glossary/sql/asc) or [descending](codex:glossary/sql/desc) order.

## Usage

By default, `ORDER BY` sorts in ascending order.

```sql
-- Sort by name A-Z
SELECT * FROM users ORDER BY name;

-- Sort by age oldest to youngest
SELECT * FROM users ORDER BY age DESC;
```

## Multiple Columns

You can sort by multiple columns. If the first column has duplicate values, the second column will be used to break the tie.

```sql
SELECT * FROM users ORDER BY last_name ASC, first_name ASC;
```