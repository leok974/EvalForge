## Concept
When making complex changes to a database, you wrap your queries in a **Transaction** (`BEGIN` and `COMMIT`). If something goes wrong, you can `ROLLBACK` the entire transaction.

But sometimes, you only want to roll back *part* of a transaction. That's what a **Savepoint** is for. A `SAVEPOINT` creates a marker within the transaction.

## Why It Matters
Savepoints are powerful for long scripts or programmatic migrations. If step 1 succeeds, but step 2 throws an error, you don't necessarily want to abandon step 1. You can `ROLLBACK TO SAVEPOINT`, retry step 2, and then finally `COMMIT`.

## Syntax Pattern
```sql
BEGIN;

-- Do some work
UPDATE table SET col = 1;

SAVEPOINT my_savepoint_name;

-- Do some risky work
UPDATE table SET col = 2; -- Uh oh, mistake!

-- Rollback the risky work, keeping the first work
ROLLBACK TO SAVEPOINT my_savepoint_name;

COMMIT;
```

## Common Mistake
Thinking that `ROLLBACK TO SAVEPOINT` ends the transaction. It doesn't! It just rewinds the transaction back to that marker. You are still inside the transaction block and must eventually issue a `COMMIT` or a full `ROLLBACK`.
