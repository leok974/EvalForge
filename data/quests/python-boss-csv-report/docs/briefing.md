# Briefing: BOSS: CSV Reporter

## The Mission

You've been promoted to lead the Data Logistics division. Your first task is to automate weekly sales reports. You receive raw CSV files with sales data, and need a tool that parses those files, computes summary statistics, and writes a plain-text summary report.

This is a **BOSS LEVEL** quest — combine everything you've learned about CSV parsing, file handling, and error handling.

## Input Format

The input CSV has exactly two columns:

| Column  | Type  | Description              |
|---------|-------|--------------------------|
| `id`    | int   | Record identifier        |
| `sales` | float | Sales amount for this record |

Example (`sales.csv`):
```
id,sales
1,100
2,200
3,300
```

## Objectives

Implement `generate_report(input_csv: str, output_report: str)` in `task.py`:

1. **Read** the input CSV using `csv.DictReader`. Cast the `sales` column to `float`.
2. **Compute** three statistics:
   - `TOTAL_SALES` — sum of all sales values
   - `AVG_SALES` — average of all sales values
   - `COUNT` — number of records
3. **Write** the report to `output_report` as a **plain text file** with exactly these three lines:
   ```
   TOTAL_SALES=600.00
   AVG_SALES=200.00
   COUNT=3
   ```
   Monetary values use 2 decimal places (`.2f`). `COUNT` is an integer.
4. **Print to stdout**:
   - `REPORT_GENERATED` — after successfully writing the report
   - `INPUT_MISSING` — if the input file does not exist (return immediately, do not raise)

## Constraints

- Standard library only — no `pandas`.
- Use `csv.DictReader` to read the input.
- The output file is **plain text** (not CSV). Write it with `open(..., "w")`.
