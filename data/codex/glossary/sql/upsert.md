# upsert

**UPSERT** (a portmanteau of "update" and "insert") is a database operation that either inserts a new row or updates an existing one if a conflict occurs (usually on a primary key or unique index).

## SQLite Implementation

In SQLite, UPSERT is implemented using the `ON CONFLICT` clause.

## Syntax

```sql
INSERT INTO table_name (cols...)
VALUES (vals...)
ON CONFLICT (target_col)
DO UPDATE SET col = excluded.col;
```

- **ON CONFLICT**: Specifies the column(s) that trigger the conflict.
- **DO UPDATE SET**: Defines what happens to the existing row.
- **excluded**: A special table name used to reference the values that were part of the `INSERT` statement but were rejected due to the conflict.
