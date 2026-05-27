# Hints: Data Forge

## Hint 1 — Loading CSV rows

Use `csv.DictReader` inside a `with open(...)` block. Cast each field to the right type before appending to the list:

```python
rows.append({
    "item":  row["item"],
    "qty":   int(row["qty"]),
    "price": float(row["price"]),
})
```

Return the list after the loop.

## Hint 2 — Accumulating revenue per item

Initialize an empty dict, then add `qty × price` for each row:

```python
totals = {}
for row in rows:
    item = row["item"]
    totals[item] = totals.get(item, 0.0) + row["qty"] * row["price"]
return totals
```

`dict.get(item, 0.0)` handles the first occurrence of each item without raising a `KeyError`.

## Hint 3 — Top K items by revenue

Sort the dict's `(item, revenue)` pairs by revenue descending, then slice:

```python
ranked = sorted(revenue.items(), key=lambda x: x[1], reverse=True)
return ranked[:k]
```

`revenue.items()` gives pairs; `key=lambda x: x[1]` sorts by the second element (revenue); `reverse=True` puts the highest first; `[:k]` takes only the top `k`.
