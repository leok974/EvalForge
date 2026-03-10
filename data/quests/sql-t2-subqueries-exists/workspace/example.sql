-- Example: Finding employees with high login counts
-- Using EXISTS to check a related table
SELECT name
FROM employees e1
WHERE EXISTS (
  SELECT 1 
  FROM user_logins ul 
  WHERE ul.user_id = e1.id 
  AND ul.login_count > 5
);
