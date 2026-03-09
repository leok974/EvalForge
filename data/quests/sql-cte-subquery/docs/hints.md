# Hints: Logical Building Blocks

## Hint 1 — Concept
Use the `WITH` clause to define your [CTE](glossary/sql/cte) at the very beginning of your query.
`WITH active_users AS (SELECT * FROM users WHERE is_active = 1)`

## Hint 2 — Joining
After defining the CTE, you can use it exactly like a regular table in your main [SELECT](glossary/sql/select) statement.
`FROM active_users JOIN orders ON active_users.id = orders.user_id`

## Hint 3 — The Solution
Your final query should look something like this:
```sql
WITH active_users AS (
  SELECT * FROM users WHERE is_active = 1
)
SELECT
  active_users.name AS user_name,
  SUM(orders.total_cents) AS total_spend
FROM active_users
JOIN orders ON active_users.id = orders.user_id
GROUP BY active_users.name;
```
This isolates the "active user" logic from the "spend calculation" logic.
