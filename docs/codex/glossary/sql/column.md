---
id: glossary/sql/column
level: beginner
related:
- codex:glossary/sql/table
- codex:glossary/sql/row
tags:
- fundamentals
- structure
title: Column
world: sql
---

# Column

## Definition
A **Column** (also called a **field** or **attribute**) is a set of data values of a particular type, representing a specific property shared by every row in a table.

## Why It Matters
Columns define **what** kind of information a table can store. In a `products` table, columns like `name`, `price_cents`, and `category` ensure that every product has a name and a price that can be easily compared or calculated.

## Mental Model
In a spreadsheet, columns are the vertical sections topped by a header. They define the type of data (e.g., "The 'Age' column only contains numbers").

## Example
```sql
-- Select only two specific columns instead of the entire row
SELECT name, email 
FROM users;
```

## Pitfalls
- **Missing Columns**: If you try to `SELECT` a column name that doesn't exist in the table, the query will fail immediately.
- **Data Type Mismatch**: You cannot store a long paragraph of text in a column that was created to only hold numbers.

## Related
- Table: The structure that organizes columns and rows.
- Row: The individual records that fill the columns with data.