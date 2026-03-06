-- Task: Retrieve active users only.
-- Return: id, name, city for all users where is_active = 1,
-- ordered by name ascending.

-- TODO: Write your SELECT statement below
SELECT id, name, city
FROM users
WHERE is_active = 1
ORDER BY name ASC;
