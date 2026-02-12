"""
Quest: python-data-forge

Parse a CSV fixture and compute revenue per item.

Fixture: fixtures/sales.csv (columns: date,item,qty,price)

Requirements:
- load_sales(path) -> list[dict] with keys: item (str), qty (int), price (float)
- revenue_by_item(rows) -> dict[item] = revenue (float), where revenue += qty*price
- top_items(revenue, k) -> list[(item, revenue)] sorted by:
    1) revenue desc
    2) item asc
- main() loads fixtures/sales.csv and prints the top 2 items as:
    apple=10.50
    banana=6.40
  (two decimals)
"""

from __future__ import annotations

from pathlib import Path


def load_sales(path: str | Path) -> list[dict]:
  raise NotImplementedError("TODO: implement load_sales(path)")


def revenue_by_item(rows: list[dict]) -> dict[str, float]:
  raise NotImplementedError("TODO: implement revenue_by_item(rows)")


def top_items(revenue: dict[str, float], k: int) -> list[tuple[str, float]]:
  raise NotImplementedError("TODO: implement top_items(revenue, k)")


def main() -> None:
  here = Path(__file__).resolve()
  quest_root = here.parents[1]  # workspace/ -> quest root
  path = quest_root / "fixtures" / "sales.csv"

  rows = load_sales(path)
  rev = revenue_by_item(rows)
  top2 = top_items(rev, 2)

  for name, value in top2:
    print(f"{name}={value:.2f}")


if __name__ == "__main__":
  main()
