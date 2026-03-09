-- example.sql (reference)
-- This demonstrates multi-key ORDER BY.
-- It is NOT the quest answer.

SELECT
  name,
  age
FROM users
ORDER BY age DESC, name ASC;
