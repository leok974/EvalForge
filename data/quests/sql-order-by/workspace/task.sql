-- sql-order-by
-- TASK:
-- Produce a clean directory of users sorted for a printed roster.
--
-- Output columns (exact order):
--   city, name
--
-- Rules:
-- - Include all rows (no WHERE needed)
-- - Sort by city ascending
-- - For users in the same city, sort by name ascending
--
-- TODO:
-- Update the query below so it matches the required output exactly.

SELECT
  city,
  name
FROM users
ORDER BY city ASC;
