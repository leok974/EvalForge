-- sql-where
-- TASK:
-- Return only ACTIVE users from Detroit.
--
-- Output columns (exact order):
--   name, city
--
-- Rules:
-- - Filter: city = 'Detroit'
-- - Filter: is_active = 1
-- - Sort by name ascending
--
-- TODO:
-- Update the query below so it matches the required output exactly.

SELECT
  name,
  city
FROM users
ORDER BY name ASC;
