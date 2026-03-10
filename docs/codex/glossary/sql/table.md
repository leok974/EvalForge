---
title: Table
id: glossary/sql/table
world: sql
level: beginner
tags: [fundamentals, structure]
related:
  - codex:glossary/sql/row
  - codex:glossary/sql/column
  - codex:glossary/sql/select
---

# Table

## Definition
A **Table** is a collection of related data entries in a database, organized into a structured format of **rows** and **columns**. It is the fundamental building block of a relational database.

## Why It Matters
Tables act as the containers for your information. In a store database, you might have one table for `users`, another for `products`, and another for `orders`. Keeping different types of information in separate tables allows the database to remain organized and efficient.

## Mental Model
Think of a table like a single sheet in a spreadsheet (like Excel or Google Sheets).
- The name of the sheet is the **Table Name**.
- The vertical lists are the **Columns** (attributes).
- The horizontal entries are the **Rows** (individual records).

## Example
```sql
-- See the structure and content of the users table
SELECT * FROM users LIMIT 5;
```

## Pitfalls
- **Mismatched types**: Every column in a table has a specific data type (like integer or text) that cannot be mixed within the same column.
- **Naming conflicts**: You cannot have two tables with the same name in the same database schema.

## Related
- Row: An individual record within the table.
- Column: A specific attribute shared by all rows in the table.
