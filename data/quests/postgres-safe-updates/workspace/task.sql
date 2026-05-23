-- Starter code for Safe Updates
-- 1. We need to give Bob a raise.
-- 2. Update his salary to 125000 in the employees table.
-- 3. ALWAYS use a WHERE clause so you don't update everyone!
-- 4. End with a SELECT statement to verify the change.

-- NOTE: This is a safe sandbox environment. Your changes will rollback
-- automatically after evaluation, so feel free to experiment.

UPDATE employees
SET salary = 125000
-- TODO: Add the missing WHERE clause so ONLY Bob is updated

-- Verify the update:
SELECT name, salary FROM employees WHERE name = 'Bob';
