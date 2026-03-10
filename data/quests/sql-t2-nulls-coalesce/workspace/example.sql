-- Example: Demonstrating COALESCE for data cleaning
-- This query returns the hire date or 'Unknown' if not provided
SELECT 
  name, 
  COALESCE(hire_date, 'Unknown') AS start_date
FROM employees;
