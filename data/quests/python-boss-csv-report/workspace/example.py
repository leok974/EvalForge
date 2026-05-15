import csv
from pathlib import Path

def generate_report(input_csv: str, output_report: str):
    """Read a CSV, compute totals per category, write a summary report."""
    rows = []
    with open(input_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    totals = {}
    for row in rows:
        cat = row.get("category", "unknown")
        totals[cat] = totals.get(cat, 0) + int(row.get("amount", 0))

    with open(output_report, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "total"])
        for cat, total in sorted(totals.items()):
            writer.writerow([cat, total])
