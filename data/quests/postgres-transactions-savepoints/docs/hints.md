In this exercise, we are exploring partial rollbacks.

## Hint 1 — Setting the Savepoint
Check the starter code comments. Under Step 2, type `SAVEPOINT before_disaster;`.

## Hint 2 — Recovering from Error
Under Step 4, type `ROLLBACK TO SAVEPOINT before_disaster;`.

## Hint 3 — Implementation Note
You do not need to change the BEGIN, COMMIT, or the UPDATE statements. Just add the savepoint and rollback commands.
