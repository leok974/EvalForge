-- Example: Safe deletion test
-- This query tests a delete but undos it
BEGIN;
DELETE FROM employees WHERE id = 1;
-- Verify the row is gone (only in this session)
SELECT COUNT(*) FROM employees WHERE id = 1;
-- Bring it back!
ROLLBACK;
-- Row is restored
SELECT COUNT(*) FROM employees WHERE id = 1;
