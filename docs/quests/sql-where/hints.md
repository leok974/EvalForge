# Hints — SQL Where (Office Hours)

Try one hint, **Run**, then check **Query Result** before opening the next.

## Hint 1 — Identify the two filters
The prompt requires *two* conditions:
- city must be Detroit
- user must be active

You will need both conditions in your `WHERE` clause.

## Hint 2 — Use AND, not OR
If you write:

`city = 'Detroit' OR is_active = 1`

…you will get far too many rows.

Use `AND` so a row must satisfy both conditions.

## Hint 3 — Remember quotes for text
Detroit is text, so it must be written as:

`city = 'Detroit'`

## Hint 4 — Confirm the output columns
Even if your filter is correct, your output can still fail if:
- you return extra columns
- you swap the column order

The correct order is: `name`, then `city`.

## Hint 5 — Sorting is still required
Filtering doesn’t sort.

Add:
`ORDER BY name ASC`

## Hint 6 — Use the example as a pattern
`example.sql` demonstrates the structure of `WHERE + ORDER BY`.  
Apply the same structure, but with the quest’s required filters.
