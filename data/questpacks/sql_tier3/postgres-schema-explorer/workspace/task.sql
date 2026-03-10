-- Mission: Verify the PostgreSQL Workbench capabilities.
-- 1. Use the "Database" tab on the left to explore the schema.
-- 2. Find the "employees" table and note its columns.
-- 3. Write a query to list all employees in 'Engineering'.

-- Write your query below:
SELECT 
    -- TODO: return name and email
FROM employees
WHERE -- TODO: filter by 'Engineering' department
ORDER BY name;
