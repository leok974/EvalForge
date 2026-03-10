---
title: ON
id: glossary/sql/on
world: sql
level: beginner
tags: [fundamentals, syntax, relations]
related:
  - codex:glossary/sql/join
  - codex:glossary/sql/where
---

# ON

## Definition
The `ON` clause specifies the **join condition**—the rule used to determine which rows from one table match rows in another. It serves as the "logical bridge" between tables.

## Why It Matters
Without an `ON` clause, a join has no instructions on how to link data. An incorrect `ON` clause will either return no data or, more dangerously, link the wrong records together (e.g., showing the wrong customer for an order).

## Mental Model
Compare `ON` to `WHERE`:
- `ON` describes how to **combine** tables.
- `WHERE` describes how to **filter** the resulting rows.

## Example
```sql
-- Linking order items to their parent products
SELECT 
  order_items.qty,
  products.name
FROM order_items
JOIN products ON order_items.product_id = products.id;
```

## Pitfalls
- **Linking wrong columns**: Ensure you are linking Primary Keys to Foreign Keys (e.g., `users.id = orders.user_id`).
- **Filtering in ON**: While you *can* put filters in `ON`, it is usually cleaner to keep them in `WHERE` unless you are dealing with specific `LEFT JOIN` logic.

## Related
- JOIN: The clause that requires the ON condition.
- WHERE: Used to filter rows after they have been joined.
