# Hints — SQL Select (Office Hours)

Treat these like office-hours guidance: try one hint, **Run**, and check **Query Result** before opening the next.

<details>
  <summary><strong>Hint 1 — Start with the column contract</strong></summary>

Before worrying about sorting, make sure you're returning the *right shape*.

This quest requires **exactly two columns**, in this exact order:

1) `name`
2) `city`

If you return only one column (or swap the order), the result will be considered incorrect even if the data "looks close."

</details>

<details>
  <summary><strong>Hint 2 — Confirm the data source</strong></summary>

Now ask: "Where do those columns live?"

They are in the `users` table. Your query must include:

- `FROM users`

If you select from the wrong table, you may still get a valid SQL query — but it won't answer the question being asked.

</details>

<details>
  <summary><strong>Hint 3 — Don't add extra conditions</strong></summary>

The prompt asks for a directory of users. That means **include all rows**.

So for this particular quest:
- You do **not** need a `WHERE` clause.

If you added filtering, remove it and re-run.

</details>

<details>
  <summary><strong>Hint 4 — Order is not automatic in SQL</strong></summary>

This is a key SQL idea: tables have no guaranteed row order.

If the quest expects alphabetical results, you must request them explicitly with:

- `ORDER BY name ASC`

Without an `ORDER BY`, your query may sometimes *appear* sorted, but that's accidental — and tests can fail unpredictably.

</details>

<details>
  <summary><strong>Hint 5 — Do a careful final audit in Query Result</strong></summary>

After you run your query, check these two things:

1) Column headers are `name`, then `city` (not swapped)
2) Rows are sorted by `name` ascending

If either is off, fix the **SELECT column list** or the **ORDER BY** clause and run again.

</details>

<details>
  <summary><strong>Hint 6 — Use the example as a pattern, not an answer</strong></summary>

`example.sql` is there to demonstrate the *structure* of a well-formed query (SELECT → FROM → ORDER BY).

It is **not** the solution to this quest.

Your job is to apply the same structure to the specific requirements:
- select the two required columns
- from the correct table
- sorted by the required key

</details>
