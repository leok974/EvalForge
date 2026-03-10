**Quest: Transactions & ROLLBACK**

### The Mission
Safety first! One of the most critical skills for a database administrator is the ability to test a change and undo it if something sounds wrong.

Demonstrate [atomicity](glossary/sql/atomicity) by creating a temporary employee and then undoing the operation.

### Requirements
1. **Start**: Start a new [transaction](glossary/sql/transaction) using the `BEGIN;` command.
2. **Action**: `INSERT` a new employee into the `employees` table with `id = 99` and `name = 'Test'`.
3. **Undo**: Use the [ROLLBACK](glossary/sql/rollback) command to discard the change.
4. **Verification**: After the rollback, run a `SELECT COUNT(*) FROM employees WHERE id = 99;`.
5. **Success**: The quest is successful if the count returns `0`.
