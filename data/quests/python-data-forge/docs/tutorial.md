# Tutorial: CSV Loading, Dict Accumulation, and Top-K Sorting

This quest builds the classic data-processing pipeline: **load → aggregate → rank**. Each function handles one stage.

## Stage 1 — Loading CSV with DictReader

`csv.DictReader` reads each row as a dictionary keyed by the column headers. All values arrive as strings — cast them to the correct type immediately.

```python
import csv
from pathlib import Path

def load_data(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "name":  row["name"],
                "count": int(row["count"]),    # string → int
                "value": float(row["value"]),  # string → float
            })
    return rows
```

Key points:
- Open the file inside a `with` block so it closes automatically.
- Build an empty list before the loop; `append` inside; `return` after.
- Cast `qty` → `int` and `price` → `float` at load time so later math is clean.

## Stage 2 — Accumulating into a Dict

To sum a value per category, use a running-total dict:

```python
totals = {}
for row in rows:
    key = row["name"]
    totals[key] = totals.get(key, 0.0) + row["value"]
```

`dict.get(key, 0.0)` returns `0.0` the first time a key appears, avoiding a `KeyError`. Revenue per row = `qty × price`:

```python
totals[item] = totals.get(item, 0.0) + row["qty"] * row["price"]
```

## Stage 3 — Sorting and Taking Top K

To get the top `k` items by value:

```python
ranked = sorted(revenue.items(), key=lambda x: x[1], reverse=True)
top_k = ranked[:k]
```

- `revenue.items()` yields `(item, revenue)` pairs.
- `key=lambda x: x[1]` sorts by the revenue value (the second element).
- `reverse=True` puts the highest value first.
- `[:k]` slices off the first `k` results.

## Putting the Pipeline Together

```python
rows   = load_sales("fixtures/sales.csv")
rev    = revenue_by_item(rows)
top2   = top_items(rev, 2)
# → [("apple", 10.50), ("banana", 6.40)]
```

Each function is independent and testable on its own.
