# Example: load attendance data and compute hours per employee.
# Same three-stage pipeline as the quest (load → accumulate → top-k),
# applied to a different domain so you can see the pattern without
# seeing the solution.
#
# Fixture columns: date (str), employee (str), hours (float)

from __future__ import annotations

import csv
from pathlib import Path


def load_attendance(path: str | Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "employee": row["employee"],
                "hours": float(row["hours"]),
            })
    return rows


def hours_by_employee(rows: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in rows:
        emp = row["employee"]
        totals[emp] = totals.get(emp, 0.0) + row["hours"]
    return totals


def top_workers(totals: dict[str, float], k: int) -> list[tuple[str, float]]:
    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return ranked[:k]
