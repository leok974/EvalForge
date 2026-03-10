# Hints: Transactions & Rollback

## Hint 1 — Starting Safe
To group multiple commands into a single atomic unit, start with `BEGIN TRANSACTION;` (or just `BEGIN;`).

## Hint 2 — The Escape Hatch
If you change your mind or an error occurs, `ROLLBACK;` will undo every change made since the last `BEGIN`.

## Hint 3 — The Solution
```sql
BEGIN;
UPDATE employees SET salary = salary - 50000 WHERE id = 1;
UPDATE employees SET salary = salary + 50000 WHERE id = 2;
ROLLBACK;

SELECT id, name, salary FROM employees ORDER BY id ASC;
```
Check the output—Alice and Bob should still have their original salaries!
