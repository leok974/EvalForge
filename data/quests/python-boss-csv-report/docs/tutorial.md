# Tutorial: Working with CSV Files

CSV (Comma Separated Values) is the universal format for data exchange. Python's `csv` module provides classes to read and write tabular data.

## Reading with DictReader
Using `csv.DictReader` is often better than a standard reader because it maps each row to a dictionary, using the headers as keys.

```python
import csv

with open('data.csv', mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['sector'], row['value'])
```

## Writing with DictWriter
Similarly, `csv.DictWriter` allows you to write dictionaries directly to a file.

```python
with open('report.csv', mode='w', newline='') as f:
    fieldnames = ['sector', 'total']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerow({'sector': 'Alpha', 'total': 100})
```

## Path Management
Use the `pathlib` module to handle file paths robustly across different operating systems.

```python
from pathlib import Path
input_path = Path("workspace/fixtures/input.csv")
```

## Aggregation Strategy
1. Initialize a summary dictionary (e.g., `totals = {}`).
2. Loop through the raw rows.
3. Update the summary (e.g., `totals[sector] = totals.get(sector, 0) + value`).
4. Format the final results for the writer.
