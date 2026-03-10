---
id: glossary/sql/delete
title: delete
world: sql
---

# delete

The `DELETE` statement is used to remove existing records from a table.

## Usage

```sql
DELETE FROM users WHERE id = 10;
```

## Warning

**Always use a WHERE clause!** If you omit the `WHERE` clause, the database will delete **every single row** in the table.