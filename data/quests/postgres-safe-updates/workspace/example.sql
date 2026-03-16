-- Example: The Safe Update Pattern

-- Step 1: Inspect the target row(s) FIRST to ensure your WHERE is correct.
SELECT id, name, department_id 
FROM employees 
WHERE name = 'Alice';

-- Step 2: Perform the Update, using the specific ID or precise condition.
UPDATE employees
SET department_id = 2
WHERE name = 'Alice';
-- CAUTION: If you skip the WHERE clause, EVERY row is updated!

-- Step 3: Verify the change.
SELECT id, name, department_id 
FROM employees 
WHERE name = 'Alice';
