-- Example SQL for Schema Exploration
-- This query demonstrates how you can filter employees by department 
-- using a JOIN and only return specific columns.

SELECT 
    e.name, 
    e.email,
    d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.name = 'Engineering';

-- Pro-tip: You can use the Database Explorer to find all valid departments!
