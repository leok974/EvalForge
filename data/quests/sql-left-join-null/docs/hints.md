# Hints: Finding the Gaps

## Hint 1 — Concept
Use a [LEFT JOIN](glossary/sql/join) between `users` and `orders`. This ensures that users without orders are still included in your result set, with `NULL` in the order columns.

## Hint 2 — Connection
Join the tables using the `id` from `users` and the `user_id` from `orders`.
`FROM users LEFT JOIN orders ON users.id = orders.user_id`

## Hint 3 — The Answer
To find only the users with no orders, filter for rows where the `orders.id` is [NULL](glossary/sql/null).
```sql
SELECT
  users.name AS user_name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
```
This reveals the "gaps" where no relationship exists.
