# Tutorial: CSV Reading and Plain-Text Reporting

This quest combines four skills: CSV parsing, type casting, arithmetic, and plain-text file writing.

## Reading CSV with DictReader

`csv.DictReader` parses each row as a dictionary keyed by the column headers.

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["id"], row["sales"])  # both are strings
```

**Important:** every CSV value arrives as a string — cast before arithmetic:

```python
sales = float(row["sales"])
```

## Aggregating Values

Accumulate a running total and a count in a loop:

```python
total = 0.0
count = 0

with open(input_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += float(row["sales"])
        count += 1

avg = total / count if count > 0 else 0.0
```

## Writing a Plain-Text Report

Write each metric as a `KEY=VALUE` line using an f-string. Use `:.2f` for two decimal places:

```python
with open(output_report, "w", encoding="utf-8") as f:
    f.write(f"TOTAL_SALES={total:.2f}\n")
    f.write(f"AVG_SALES={avg:.2f}\n")
    f.write(f"COUNT={count}\n")
```

This is a **plain text file**, not a CSV — do not use `csv.DictWriter` here.

## Printing Sentinels to Stdout

After writing the report, signal success by printing a sentinel to stdout:

```python
print("REPORT_GENERATED")
```

The grader checks `stdout` for this line. It is separate from the report file.

## Handling a Missing Input File

Check whether the input exists before opening it. If it's missing, print the error sentinel and return immediately:

```python
from pathlib import Path

def generate_report(input_csv: str, output_report: str) -> None:
    if not Path(input_csv).exists():
        print("INPUT_MISSING")
        return

    # ... read, aggregate, write ...

    print("REPORT_GENERATED")
```

Do not raise an exception for the missing-file case — print `INPUT_MISSING` and return.
