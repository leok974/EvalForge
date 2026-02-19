import argparse
import json
import sys
from pathlib import Path

BUDGET_PATH = Path("docs/audits/golden_budget.json")
AUDIT_PATH = Path("docs/audits/GOLDEN_COVERAGE_AUDIT.json")

def load_json(p: Path):
    if not p.exists():
        print(f"❌ File not found: {p}")
        sys.exit(1)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save_budget(budget):
    with open(BUDGET_PATH, "w", encoding="utf-8") as f:
        json.dump(budget, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Ratchet golden budget")
    parser.add_argument("--tighten", type=int, help="Decrease max_spec by N")
    parser.add_argument("--check", action="store_true", help="Just check if within budget")
    
    args = parser.parse_args()
    
    budget = load_json(BUDGET_PATH)
    audit = load_json(AUDIT_PATH)
    
    max_spec = budget.get("max_spec", 999)
    current_spec = audit.get("summary", {}).get("with_golden_spec", 0)
    
    print(f"📊 Current Spec Count: {current_spec}")
    print(f"🎯 Max Allowed: {max_spec}")
    
    if args.tighten:
        new_max = max_spec - args.tighten
        if new_max < current_spec:
            print(f"⚠️ Cannot tighten to {new_max} because current is {current_spec}. Fix quests first!")
            sys.exit(1)
        
        budget["max_spec"] = new_max
        save_budget(budget)
        print(f"🔒 Tightened budget. New max_spec: {new_max}")
        sys.exit(0)

    # Verification Mode
    if current_spec > max_spec:
        print(f"❌ FAILURE: Current spec count ({current_spec}) exceeds budget ({max_spec})!")
        print("   Please convert specs to runs or revert changes.")
        sys.exit(1)
        
    print("✅ Budget check passed.")

if __name__ == "__main__":
    main()
