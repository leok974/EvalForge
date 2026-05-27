# Example: read a products.csv with columns (product, price) and write
# a plain-text summary report — same pattern as the quest, different data.
#
# Columns: product (str), price (float)
# Output lines:
#   TOTAL_PRICE=<value>
#   AVG_PRICE=<value>
#   COUNT=<n>
# Stdout sentinel: REPORT_GENERATED  (or INPUT_MISSING on bad path)

import csv
from pathlib import Path


def summarize_products(input_csv: str, output_report: str) -> None:
    if not Path(input_csv).exists():
        print("INPUT_MISSING")
        return

    total_price = 0.0
    count = 0

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                total_price += float(row["price"])
                count += 1
            except (ValueError, KeyError):
                continue

    avg_price = total_price / count if count > 0 else 0.0

    with open(output_report, "w", encoding="utf-8") as f:
        f.write(f"TOTAL_PRICE={total_price:.2f}\n")
        f.write(f"AVG_PRICE={avg_price:.2f}\n")
        f.write(f"COUNT={count}\n")

    print("REPORT_GENERATED")
