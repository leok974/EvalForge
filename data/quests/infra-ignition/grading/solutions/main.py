import sys
from pathlib import Path

def main():
    root = Path(".")
    outputs = root / "outputs"
    outputs.mkdir(exist_ok=True)
    
    # Read requirements
    # Assuming fixtures/tools.txt exists in PWD (workspace root)
    try:
        with open("fixtures/tools.txt", "r", encoding="utf-8") as f:
            req = [line.strip() for line in f if line.strip()]
            
        with open("fixtures/which.txt", "r", encoding="utf-8") as f:
            inst_lines = set(line.strip() for line in f if line.strip())
    except FileNotFoundError as e:
        print(f"Error reading fixtures: {e}", file=sys.stderr)
        sys.exit(1)

    missing = []
    for tool in req:
        if tool not in inst_lines:
            missing.append(tool)
            
    preflight = outputs / "preflight.txt"
    try:
        if missing:
            missing_str = ",".join(missing)
            with open(preflight, "w", encoding="utf-8") as f:
                f.write(f"STATUS=FAIL\nMISSING={missing_str}\n")
            print("MISSING_TOOLS", file=sys.stderr)
            sys.exit(10)
        else:
            with open(preflight, "w", encoding="utf-8") as f:
                f.write("STATUS=OK\nMISSING=\n")
            sys.exit(0)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
