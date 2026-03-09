-- example.sql (reference)
-- This demonstrates WHERE + ORDER BY on the users table.
-- It is NOT the quest answer.

SELECT
  name,
  city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
