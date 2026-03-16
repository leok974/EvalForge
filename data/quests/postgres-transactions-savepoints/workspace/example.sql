-- Example: Safe Transactions with Savepoints
-- Use Savepoints when executing a multi-step mutation where a middle step might fail.

BEGIN;
  -- We start by safely updating a record we know is correct.
  UPDATE employees SET department_id = 3 WHERE name = 'Alice';

  -- Create a savepoint before doing anything risky
  SAVEPOINT before_batch_update;

  -- Oh no, we forgot the WHERE clause again!
  UPDATE employees SET department_id = 1;

  -- We realized our mistake. We can rollback JUST the mistake.
  ROLLBACK TO SAVEPOINT before_batch_update;

  -- Alice's update is still intact. We commit it.
COMMIT;

-- FINAL STEP: Return a result set so the learner can see the state
SELECT name, department_id 
FROM employees 
WHERE name = 'Alice';
