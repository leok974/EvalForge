---
title: DELETE
id: glossary/sql/delete
world: sql
level: intermediate
tags: [fundamentals, mutation, syntax]
related:
  - codex:glossary/sql/update
  - codex:glossary/sql/where
---

# DELETE

## Definition
The `DELETE` statement is used to remove existing records from a table. It deletes the entire row, not just specific column values.

## Why It Matters
`DELETE` is used for data cleanup and privacy. When a user deletes their account or an accidental duplicate entry is found, `DELETE` ensures the database remains accurate and uncluttered.

## Core Syntax
```sql
DELETE FROM table_name
WHERE condition;
```

## Example
```sql
-- Remove cancelled orders from the database
DELETE FROM orders
WHERE status = 'cancelled';
```

## Pitfalls
- **Missing WHERE Clause**: Like `UPDATE`, if you omit the `WHERE` clause, **all rows** in the table will be deleted, leaving you with an empty table.
- **Foreign Key Constraints**: You cannot delete a row if it is being referenced by another table (e.g., you cannot delete a `user` who still has `orders` unless the database is set to "cascade delete").

## Related
- WHERE: Essential for specifying which rows to remove.
- UPDATE: Changes row data without removing the row itself.
