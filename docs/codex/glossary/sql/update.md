---
id: glossary/sql/update
title: update
world: sql
---

# update

The `UPDATE` statement is used to modify existing records in a table. It is always used with a `SET` clause to specify the new values and usually a `WHERE` clause to limit which rows are affected.

## Usage

```sql
UPDATE employees
SET salary = salary * 1.05
WHERE department = 'Sales';
```

## Warning

**Always use a WHERE clause!** If you omit the `WHERE` clause, the database will update **every single row** in the table, which is rarely what you want.