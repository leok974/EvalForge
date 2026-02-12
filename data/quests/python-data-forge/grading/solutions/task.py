from __future__ import annotations

import csv
from pathlib import Path


def load_sales(path: str | Path) -> list[dict]:
  p = Path(path)
  rows: list[dict] = []
  with p.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
      rows.append(
        {
          "item": str(r["item"]),
          "qty": int(r["qty"]),
          "price": float(r["price"]),
        }
      )
  return rows


def revenue_by_item(rows: list[dict]) -> dict[str, float]:
  out: dict[str, float] = {}
  for r in rows:
    item = r["item"]
    revenue = float(r["qty"]) * float(r["price"])
    out[item] = out.get(item, 0.0) + revenue
  return out


def top_items(revenue: dict[str, float], k: int) -> list[tuple[str, float]]:
  items = list(revenue.items())
  items.sort(key=lambda t: (-t[1], t[0]))
  return items[:k]


def main() -> None:
  here = Path(__file__).resolve()
  quest_root = here.parents[2]  # grading/solutions -> grading -> quest root
  path = quest_root / "fixtures" / "sales.csv"

  rows = load_sales(path)
  rev = revenue_by_item(rows)
  top2 = top_items(rev, 2)

  for name, value in top2:
    print(f"{name}={value:.2f}")


if __name__ == "__main__":
  main()
