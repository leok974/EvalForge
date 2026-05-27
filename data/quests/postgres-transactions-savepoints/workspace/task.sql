-- Starter code for Transactions & Savepoints
-- 1. We are giving Charlie a raise to 100000.
-- 2. Then creating a savepoint.
-- 3. Then making a "bad" update that ruins everyone's salary.
-- 4. Then rolling back JUST the bad update.
-- 5. Finally, committing the transaction so Charlie still gets his raise.
--
-- Follow the step-by-step instructions below.

BEGIN;

-- Step 1. Give Charlie a raise to 100000
UPDATE employees SET salary = 100000 WHERE name = 'Charlie';

-- Step 2. Create a savepoint named 'before_disaster'
-- TODO: Add SAVEPOINT here

-- Step 3. The bad update! (Sets everyone's salary to 0)
UPDATE employees SET salary = 0;

-- Step 4. Rollback to the savepoint
-- TODO: Add ROLLBACK TO SAVEPOINT here

-- Step 5. Commit the transaction
COMMIT;

-- Verify the final state. Charlie should have 100000, and Bob should still have 115000.
SELECT name, salary FROM employees WHERE name IN ('Charlie', 'Bob') ORDER BY name;
