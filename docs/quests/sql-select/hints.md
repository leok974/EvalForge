# Hints — SQL Select (Office Hours)

Treat these like office-hours guidance: try one hint, **Run**, and check **Query Result** before opening the next.

## Hint 1 — Start with the column contract
Before worrying about sorting, make sure you're returning the *right shape*.

This quest requires **exactly two columns**, in this exact order:
- `name`
- `city`

If you return only one column (or swap the order), the result will be considered incorrect even if the data "looks close."

## Hint 2 — Confirm the data source
Now ask: "Where do those columns live?"

They are in the `users` table. Your query must include:
- `FROM users`

If you select from the wrong table, you may still get a valid SQL query — but it won't answer the question being asked.

## Hint 3 — Don't add extra conditions
The prompt asks for a directory of users. That means **include all rows**.

So for this particular quest:
- You do **not** need a `WHERE` clause.

If you added filtering, remove it and re-run.

## Hint 4 — Order is not automatic in SQL
Tables do not guarantee row order. If the quest expects alphabetical results, you must request them explicitly with:
- `ORDER BY name ASC`

Without `ORDER BY`, your output may sometimes look sorted, but that's accidental — and tests can fail unpredictably.

## Hint 5 — Do a careful final audit in Query Result
After you run your query, check:

1. Column headers are `name`, then `city` (not swapped)
2. Rows are sorted by `name` ascending

If either is off, adjust your **SELECT column list** or your **ORDER BY** clause and re-run.

## Hint 6 — Use the example as a pattern, not an answer
`example.sql` demonstrates the *structure* of a well-formed query (SELECT → FROM → ORDER BY).
It is **not** the quest answer.

Your job is to apply the same structure to the specific requirements:
- select the two required columns
- from the correct table
- sorted by the required key
