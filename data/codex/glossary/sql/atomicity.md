# atomicity

**Atomicity** is the "A" in **ACID**. it guarantees that a series of database operations (a [transaction](glossary/sql/transaction)) are treated as a single "atom" or unit.

## The Rule

**All or Nothing.** 
- If every statement in a transaction succeeds, the entire unit is committed to the database.
- If even one statement fails, the entire transaction is rolled back, and the database acts as if none of the statements ever happened.

This prevents the database from ending up in a "partially updated" or inconsistent state.
