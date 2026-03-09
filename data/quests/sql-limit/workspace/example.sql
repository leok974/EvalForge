-- Reference example (not graded):
-- Return the first 5 users alphabetically.

SELECT
  id,
  name,
  city
FROM users
ORDER BY name ASC
LIMIT 5;
