# Hints: BOSS: CSV Reporter

## Hint 1 — Concept

Check whether the input file exists before opening it. Use `Path(input_csv).exists()` from `pathlib`. If it doesn't exist, print `INPUT_MISSING` and `return` immediately — no exception needed.

## Hint 2 — Guided

CSV values are always strings. Cast the `sales` column to `float` before adding it to your running total:

```python
total += float(row["sales"])
count += 1
```

Then compute the average: `avg = total / count`.

## Hint 3 — The Solution

The output file is **plain text** — use f-strings, not `csv.DictWriter`:

```python
with open(output_report, "w", encoding="utf-8") as f:
    f.write(f"TOTAL_SALES={total:.2f}\n")
    f.write(f"AVG_SALES={avg:.2f}\n")
    f.write(f"COUNT={count}\n")
print("REPORT_GENERATED")
```

`:.2f` formats a float to exactly 2 decimal places. The `REPORT_GENERATED` sentinel goes to **stdout** — not into the report file.
