"""
Quest: python-data-forge

Parse a CSV fixture and compute revenue per item.
"""

from __future__ import annotations
import csv
from pathlib import Path


def load_sales(path: str | Path) -> list[dict]:
  """Load CSV and return list of dicts with keys: item, qty, price."""
  rows = []
  with open(path) as f:
    reader = csv.DictReader(f)
    for row in reader:
      rows.append({
        'item': row['item'],
        'qty': int(row['qty']),
        'price': float(row['price'])
      })
  return rows


def revenue_by_item(rows: list[dict]) -> dict[str, float]:
  """Calculate total revenue per item."""
  revenue = {}
  for row in rows:
    item = row['item']
    rev = row['qty'] * row['price']
    revenue[item] = revenue.get(item, 0.0) + rev
  return revenue


def top_items(revenue: dict[str, float], k: int) -> list[tuple[str, float]]:
  """Return top k items sorted by revenue desc, then item name asc."""
  items = sorted(revenue.items(), key=lambda x: (-x[1], x[0]))
  return items[:k]


def main() -> None:
  here = Path(__file__).resolve()
  
  # When running in runner: fixtures are in ./fixtures (relative to script)
  # When running locally in dev: fixtures are in workspace/fixtures
  
  # Valid path for solution (assuming solution file is simulated in workspace root)
  path = here.parent / "fixtures" / "sales.csv"

  rows = load_sales(path)
  rev = revenue_by_item(rows)
  top2 = top_items(rev, 2)

  for name, value in top2:
    print(f"{name}={value:.2f}")


if __name__ == "__main__":
  main()