---
title: JOIN
id: glossary/sql/join
world: sql
level: beginner
tags: [fundamentals, relations, syntax]
related:
  - codex:glossary/sql/on
  - codex:glossary/sql/select
  - codex:glossary/sql/null
---

# JOIN

## Definition
A `JOIN` clause is used to combine rows from two or more tables based on a related column between them. It is the core mechanism for working with relational databases where data is normalized into separate tables.

## Why It Matters
In a well-designed database, information is split across tables to avoid duplication (e.g., `users` are separate from `orders`). `JOIN` allows you to reconstruct the full picture, such as finding which user placed which order.

## Syntax & Mental Model
Think of a `JOIN` as a horizontal expansion. You are taking a row from Table A and "gluing" a row from Table B onto its side where their IDs match.

- **INNER JOIN**: Returns rows only when there is a match in both tables.
- **LEFT JOIN**: Returns all rows from the left table, and the matched rows from the right table (unmatched data becomes `NULL`).

## Example
```sql
-- Combine orders and users to see who placed each order
SELECT 
  orders.id AS order_id, 
  users.name AS customer_name
FROM orders
JOIN users ON orders.user_id = users.id;
```

## Pitfalls
- **Cartesian Products**: If you forget the `ON` clause (or use a comma-join without a filter), SQL may return every possible combination of rows, leading to millions of results.
- **Ambiguous Columns**: If both tables have a column named `id`, you must prefix them (e.g., `users.id`) to avoid errors.

## Related
- ON: Defines the condition for the match.
- NULL: What appears in a `LEFT JOIN` when no match is found.
