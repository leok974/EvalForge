-- sql-select
-- TASK:
-- Return a directory of users and their city.
--
-- Output columns (exact order):
--   name, city
--
-- Rules:
-- - Include all rows
-- - Sort by name ascending

SELECT
  name,
  city
FROM users
ORDER BY name ASC;
