# transaction

A **transaction** is a sequence of one or more SQL statements that are executed as a single, logical unit of work. Transactions are governed by the **ACID** properties to ensure data integrity.

## Commands

- **BEGIN**: Starts a new transaction.
- **COMMIT**: Saves all changes made during the transaction permanently to the database.
- **ROLLBACK**: Undoes all changes made since the transaction began.

## Why use Transactions?

Imagine transferring money between bank accounts:
1. Deduct $100 from Account A.
2. Add $100 to Account B.

If the system crashes after step 1 but before step 2, the money disappears! By wrapping these in a transaction, you ensure that **either both steps happen, or neither happens**.
