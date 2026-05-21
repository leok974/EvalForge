WITH active_users AS (
  SELECT user_id, SUM(total_cents) AS total_spend
  FROM orders
  WHERE status = 'paid'
  GROUP BY user_id
  HAVING total_spend >= 5000
)
SELECT users.id, users.name AS user_name, active_users.total_spend
FROM active_users
JOIN users ON users.id = active_users.user_id
ORDER BY active_users.total_spend DESC;
