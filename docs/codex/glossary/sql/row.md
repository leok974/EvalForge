---
title: Row
id: glossary/sql/row
world: sql
level: beginner
tags: [fundamentals, structure]
related:
  - codex:glossary/sql/table
  - codex:glossary/sql/column
---

# Row

## Definition
A **Row** (also called a **record** or **tuple**) represents a single, complete set of data within a table. Each row identifies one specific item in the collection.

## Why It Matters
Rows are the actual items you are querying. If a `users` table has 1,000 users, it has 1,000 rows. When you search for "Alice," you are looking for the specific row where the `name` column is equal to "Alice."

## Mental Model
If a **Table** is a spreadsheet, a **Row** is a single horizontal entry. It contains the data for one specific user, one specific order, or one specific product.

## Example
```sql
-- Retrieve one specific row by its unique ID
SELECT * 
FROM users 
WHERE id = 1;
```

## Pitfalls
- **Empty Rows**: A row can have `NULL` values in some columns, but the row itself still exists as a record in the table.
- **Duplicates**: Unless a table has a "Unique Constraint" or a "Primary Key," it is technically possible to have duplicate rows, which can make data analysis very difficult.

## Related
- Table: The collection that contains multiple rows.
- Column: The individual fields that make up a single row.
