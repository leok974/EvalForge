# Briefing: Data Forge

## The Mission

The Reactor Core needs a pipeline to analyse raw sales data from field agents. Your mission is to build three functions that load a CSV of transactions, compute revenue per item, and identify the top sellers.

## The Data

Fixture: `fixtures/sales.csv`

| Column  | Type  | Description              |
|---------|-------|--------------------------|
| `date`  | str   | Transaction date (not used in calculations) |
| `item`  | str   | Item name                |
| `qty`   | int   | Quantity sold            |
| `price` | float | Unit price               |

First few rows:
```
date,item,qty,price
2025-01-01,apple,2,1.50
2025-01-01,banana,5,0.80
2025-01-02,apple,1,1.50
```

## Objectives

Implement three functions in `main.py`:

### `load_sales(path: str | Path) -> list[dict]`

Read the CSV and return a list of row dictionaries. Each dict must have:
- `item`: `str`
- `qty`: `int` (cast from the string in the CSV)
- `price`: `float` (cast from the string in the CSV)

Other columns (like `date`) can be ignored.

### `revenue_by_item(rows: list[dict]) -> dict[str, float]`

Compute the total revenue for each item. Revenue per row = `qty × price`. Accumulate per item name.

```python
# Given the sample data above:
# apple:  (2×1.50) + (1×1.50) + (4×1.50) = 10.50
# banana: (5×0.80) + (3×0.80) = 6.40
{"apple": 10.50, "banana": 6.40, "carrot": 2.50}
```

### `top_items(revenue: dict[str, float], k: int) -> list[tuple[str, float]]`

Return the `k` items with the highest revenue as a list of `(item, revenue)` tuples, sorted by revenue descending.

```python
top_items(rev, 2)  # → [("apple", 10.50), ("banana", 6.40)]
```

## Verification

`main()` is already implemented — it loads `fixtures/sales.csv` and prints the top 2 items as:
```
apple=10.50
banana=6.40
```

> **Tip:** See `example.py` for the same three-step pattern applied to employee attendance data.
