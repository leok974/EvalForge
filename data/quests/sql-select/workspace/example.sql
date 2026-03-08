-- example.sql
-- A correct solution example for sql-select.
-- Goal: return each user's name and city, sorted by name.

SELECT
  name,
  city
FROM users
ORDER BY name ASC;
