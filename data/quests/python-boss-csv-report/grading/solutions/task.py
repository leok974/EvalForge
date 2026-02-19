import csv
from pathlib import Path

def generate_report(input_csv: str, output_report: str):
    """
    1. Read input_csv
    2. Calculate summary stats
    3. Write report to output_report
    """
    in_path = Path(input_csv)
    if not in_path.exists():
        print("INPUT_MISSING")
        return

    total_sales = 0
    count = 0
    
    with open(in_path, "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                sales = float(row.get("sales", 0))
                total_sales += sales
                count += 1
            except ValueError:
                continue
                
    avg_sales = total_sales / count if count > 0 else 0
    
    report = f"TOTAL_SALES={total_sales:.2f}\nAVG_SALES={avg_sales:.2f}\nCOUNT={count}\n"
    
    with open(output_report, "w", encoding='utf-8') as f:
        f.write(report)
        
    print("REPORT_GENERATED")
