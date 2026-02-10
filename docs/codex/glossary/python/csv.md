---
id: glossary/python/csv
title: CSV
world: python
level: beginner
tags: [data, files, parsing]
related:
  - codex:glossary/python/parse
  - codex:glossary/python/dictionary
  - codex:glossary/python/data-pipeline
---

## Definition
**CSV (Comma-Separated Values)** is a simple text format for storing tabular data where each line represents a row and values are separated by commas. Python's `csv` module provides tools for reading and writing CSV files.

## Usage
- Read CSV files with `csv.reader()` or `csv.DictReader()`.
- Write CSV files with `csv.writer()` or `csv.DictWriter()`.
- Use DictReader/DictWriter for column-based access.

## Example
```python
import csv

# Write CSV
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age', 'email'])
    writer.writerow(['Alice', 30, 'alice@example.com'])
    writer.writerow(['Bob', 25, 'bob@example.com'])

# Read CSV
with open('users.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} is {row['age']} years old")
```

## Pitfalls

* CSV doesn't handle commas within values well unless quoted; use proper quoting settings.
* Not specifying `newline=''` on Windows can cause extra blank rows.

## Related

* Parse: CSV parsing is a form of text parsing.
* Dictionary: DictReader returns rows as dictionaries.
* Data Pipeline: CSV is common in data pipelines for ingestion.