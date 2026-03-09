-- example.sql (reference)
-- This demonstrates basic aggregate functions.
-- It is NOT the quest answer.

SELECT
  COUNT(*) AS user_count,
  AVG(age) AS average_age
FROM users;
