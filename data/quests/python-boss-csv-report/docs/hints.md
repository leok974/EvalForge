# Hints: BOSS: CSV Reporter

## Hint 1 — Concept
Start by checking if the input file exists using `Path(input_csv).exists()`. If it doesn't, your code should handle it gracefully or raise a helpful error.

## Hint 2 — Guided
In the `csv.DictReader` loop, remember that values from CSVs are always **strings**. You must convert numbers to `int` or `float` before performing calculations.

## Hint 3 — The Solution
When writing the report with `csv.DictWriter`, make sure your `fieldnames` list exactly matches the headers expected by the grader.
