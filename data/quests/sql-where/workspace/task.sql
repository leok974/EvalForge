-- Task: Retrieve active users in Detroit, age 25 or older.
-- Return: id, name, age
-- Order: By id ascending.

-- TODO: Write your SELECT statement below
SELECT id, name, age
FROM users
WHERE is_active = 1 
  AND city = 'Detroit' 
  AND age >= 25
ORDER BY id ASC;
