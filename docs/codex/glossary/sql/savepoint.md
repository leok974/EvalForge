# SQL: Savepoint

A `SAVEPOINT` allows you to establish a marker within a transaction. If an error occurs or a mistake is made after the savepoint, you can rollback to that specific marker without abandoning the entire transaction.

### Why use SAVEPOINT?
- **Partial Rollbacks**: You can try a complex or risky operation within a broader transaction.
- **Error Recovery**: In programmatic scripts, you can catch errors, rollback to the savepoint, and try an alternative approach.

### Syntax

```sql
-- Establish the savepoint
SAVEPOINT my_savepoint_name;

-- Rollback just to the savepoint
ROLLBACK TO SAVEPOINT my_savepoint_name;

-- Note: You still need to COMMIT or ROLLBACK the main transaction eventually.
```

### Example
```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;

  SAVEPOINT before_risky_update;
  
  -- We make a mistake here (e.g. updating all accounts!)
  UPDATE accounts SET balance = 0;
  
  -- Let's undo just the risky update
  ROLLBACK TO SAVEPOINT before_risky_update;

  -- The first update is still pending, now we commit it
COMMIT;
```

### Common Mistake
Forgetting that `ROLLBACK TO SAVEPOINT` does not end the transaction. You must still issue a `COMMIT` or `ROLLBACK` at the very end to finalize the transaction.
