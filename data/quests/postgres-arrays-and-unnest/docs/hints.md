In this exercise, you will learn how to flatten arrays into individual rows.

## Hint 1 — Flattening Arrays
Check out the UNNEST() function. It takes an array and returns one row per element.

## Hint 2 — Selecting from Arrays
Your SELECT clause should look like: `SELECT name, UNNEST(skills) AS skill`.

## Hint 3 — Filtering Results
Don't forget to add a WHERE clause to filter for `department_id = 1`!
