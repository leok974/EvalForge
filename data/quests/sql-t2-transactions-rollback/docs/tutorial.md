# Tutorial: Transactions & ROLLBACK

In a professional database, you often need to perform multiple operations that must either **all succeed** or **all fail**. This is called **Atomicity**, and it's managed via **Transactions**.

## Atomicity (All or Nothing)

Imagine a bank transfer:
1. Subtract $100 from Account A.
2. Add $100 to Account B.

If step 1 succeeds but step 2 fails (e.g., due to a power outage), the $100 vanishes. To prevent this, you wrap both steps in a transaction.

## Basic Transaction Lifecycle

1. **BEGIN**: Starts the transaction. All changes made after this point are "temporary" and visible only to your session.
2. **COMMIT**: Makes all temporary changes permanent.
3. **ROLLBACK**: Undoes all temporary changes and returns the database to the state it was in at the `BEGIN`.

```sql
BEGIN;
DELETE FROM accounts WHERE id = 1;
-- Something went wrong!
ROLLBACK;
-- The account is back!
```

In this quest, you will demonstrate the power of atomicity by inserting an employee within a transaction and then rolling it back to prove that the data was not permanently stored.
