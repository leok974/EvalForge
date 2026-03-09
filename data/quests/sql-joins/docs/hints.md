# Hints: Building Bridges

## Hint 1 — Concept
Use the [JOIN](glossary/sql/join) clause to connect the two tables. This typically goes right after the [FROM](glossary/sql/from) clause.

## Hint 2 — Connection
Use the [ON](glossary/sql/on) clause to tell the database how the tables relate. In this case, `orders.user_id` should equal `users.id`.

## Hint 3 — The Answer
Your query should look like this:
```sql
SELECT
  orders.id AS order_id,
  users.name AS user_name
FROM orders
JOIN users ON orders.user_id = users.id;
```
This merges the rows from both tables wherever the IDs match.
