# Hints — SQL Order By (Office Hours)

Try one hint, **Run**, and check **Query Result** before opening the next.

## Hint 1 — Start with the output contract
Make sure you return exactly two columns, in this order:
- `city`
- `name`

If you swap them, the output is wrong even if the data is correct.

## Hint 2 — One ORDER BY key is not enough
If you only sort by `city`, the names inside each city may appear in a random order.

You need a second key.

## Hint 3 — Use a comma to add the second key
Multi-key ordering uses commas:

`ORDER BY city ASC, name ASC`

## Hint 4 — Keep both sorts ascending
This quest wants alphabetical order in both dimensions.
Make sure you’re not using `DESC`.

## Hint 5 — Audit the result visually
In Query Result:
- Find a city that appears multiple times (like Austin or Detroit)
- Confirm the names under that city are alphabetically ordered
