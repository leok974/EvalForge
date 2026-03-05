# Mission: Transactions & Rollback
**Goal**:
1. Issue a `BEGIN;` or `BEGIN TRANSACTION;`.
2. Write an `INSERT` statement adding a new department or employee (e.g., `INSERT INTO employees (id, name) VALUES (99, 'Test');`).
3. Issue a `ROLLBACK;` statement to cancel the transaction.
4. Write a final query: `SELECT COUNT(*) FROM employees WHERE id = 99;` to verify the rollback worked.