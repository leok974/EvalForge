-- sql-t2-transactions-rollback
-- TASK:
-- Demonstrate atomicity by attempting a transfer but rolling it back.
--
-- Output columns (exact order):
--   id, name, salary
--
-- Rules:
-- - Begin a transaction
-- - Update Alice (ID 1): decrease salary by 50000
-- - Update Bob (ID 2): increase salary by 50000
-- - Rollback the transaction
-- - Select all employees at the end
--
-- TODO:
-- Update the script below to wrap the updates in a transaction and then undo them.

-- TODO: BEGIN TRANSACTION;

UPDATE employees SET salary = salary - 50000 WHERE id = 1;
UPDATE employees SET salary = salary + 50000 WHERE id = 2;

-- TODO: ROLLBACK;

SELECT id, name, salary FROM employees ORDER BY id ASC;
