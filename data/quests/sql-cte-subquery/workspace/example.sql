-- example.sql (reference)
-- This demonstrates a Common Table Expression (CTE).
-- It is NOT the quest answer.

WITH detroit_users AS (
  SELECT * FROM users WHERE city = 'Detroit'
)
SELECT
  COUNT(*) AS count_in_detroit
FROM detroit_users;
