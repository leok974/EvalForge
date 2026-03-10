# rollback

The `ROLLBACK` command is used to undo every change made to the database since the last [transaction](glossary/sql/transaction) was started.

## Lifecycle

1. `BEGIN;`
2. `UPDATE ...`
3. If something goes wrong: `ROLLBACK;`
4. All data returns to exactly how it was before the `BEGIN`.

## Usage in Development

Developers often use `ROLLBACK` when testing scripts or performing destructive operations to ensure they can "escape" without damaging the database if their logic is incorrect.
