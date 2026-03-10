---
title: INSERT
id: glossary/sql/insert
world: sql
level: beginner
tags: [fundamentals, mutation, syntax]
related:
  - codex:glossary/sql/update
  - codex:glossary/sql/delete
---

# INSERT

## Definition
The `INSERT INTO` statement is used to add new records (rows) to a table. It allows you to expand your database by providing data for the table's defined columns.

## Why It Matters
`INSERT` is the engine for user growth and activity. Every time a new user registers, a product is added to the catalog, or an order is placed, an `INSERT` command is running behind the scenes.

## Core Syntax
```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

## Example
```sql
-- Add a new product to the electronics category
INSERT INTO products (id, name, category, price_cents, is_discontinued)
VALUES (6, 'Bluetooth Speaker', 'electronics', 4500, 0);
```

## Pitfalls
- **Column-Value Mismatch**: The number of columns listed must exactly match the number of values provided.
- **Constraint Violations**: Trying to insert a duplicate ID for a Primary Key or a string into a numeric column will cause an error.
- **Missing Required Columns**: Forgetting a column marked as `NOT NULL` without a default value will prevent the row from being added.

## Related
- UPDATE: Modifies existing rows instead of adding new ones.
- DELETE: Removes rows from the table.
