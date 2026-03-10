---
id: glossary/sql/exists
title: exists
world: sql
---

# exists

The `EXISTS` operator is used to test for the existence of any record in a [subquery](glossary/sql/subquery). It returns `TRUE` if the subquery returns one or more records.

## Usage

`EXISTS` is often more efficient than `IN` when checking for existence because the database can stop searching as soon as it finds a single matching row.

## Example

```sql
-- Find customers who have placed at least one order
SELECT name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.id
);
```

## Anti-Pattern

In some cases, you might use `NOT EXISTS` to find records that *don't* have a match in another table (an anti-join).