-- example.sql (reference)
-- This demonstrates GROUP BY + COUNT.
-- It is NOT the quest answer.

SELECT
  city,
  COUNT(*) AS user_count
FROM users
GROUP BY city;
