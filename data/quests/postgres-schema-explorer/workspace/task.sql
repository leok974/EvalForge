-- Mission: Audit the Engineering department contact list.
-- 1. Use the "Database" tab to explore the 'employees' and 'departments' tables.
-- 2. Resolve the 'department_id' for 'Engineering'.
-- 3. Return the 'name' and 'email' of all matching employees.

SELECT 
    name, 
    email 
FROM employees 
WHERE department_id = 0 -- TODO: Filter by 'Engineering' department
ORDER BY name;
