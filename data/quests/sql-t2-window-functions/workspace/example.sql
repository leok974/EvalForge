-- Example: Assigning a global row number
-- This assigns a unique ID to every row based on salary
SELECT 
    name, 
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;
