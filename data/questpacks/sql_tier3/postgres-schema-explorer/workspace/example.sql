-- Example SQL for Schema Exploration
-- This query demonstrates how you can filter employees by department 
-- and only return specific columns.

-- We select 'name' and 'email' for the Engineering department
SELECT 
    name, 
    email 
FROM employees 
WHERE department = 'Engineering';

-- Pro-tip: You can use the Database Explorer to find all valid departments!
