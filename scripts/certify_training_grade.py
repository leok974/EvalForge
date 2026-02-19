
import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs
from scripts.audit_objectives_schema import audit_all_quests

def run_drift_check():
    """Run upgrade_objectives_state.py --check."""
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, "scripts/upgrade_objectives_state.py", "--check"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def load_budget():
    p = Path("docs/audits/golden_budget.json")
    if p.exists():
        with open(p, "r") as f:
            return json.load(f)
    return None

def certify_training_grade():
    print("(*) Starting Training-Grade Certification...")
    
    failures = []
    
    # 1. Objectives Schema
    print("\n[?] Checking Objectives Schema...")
    schema_report = audit_all_quests()
    if schema_report['invalid_quests']:
        print(f"[FAIL] {len(schema_report['invalid_quests'])} quests have invalid objectives.")
        for f in schema_report['invalid_quests']:
            failures.append(f"Schema Invalid: {f['slug']}")
    
    if schema_report['quests_with_no_objectives']:
        print(f"[FAIL] {len(schema_report['quests_with_no_objectives'])} quests have NO objectives.")
        for q in schema_report['quests_with_no_objectives']:
             failures.append(f"No Objectives: {q}")
             
    # 2. Golden Coverage & Integrity Stats
    print("\n[?] Checking Golden Coverage & Integrity...")
    
    all_slugs = get_all_quest_slugs()
    stats = {
        "run": 0,
        "state": 0,
        "spec": 0,
        "missing": 0,
        "total": len(all_slugs)
    }
    missing_list = []
    spec_list = []
    
    for slug in all_slugs:
        grading_dir = Path(f"data/quests/{slug}/grading")
        has_run = (grading_dir / "golden.run.json").exists() or (grading_dir / "golden.json").exists()
        has_state = (grading_dir / "golden.state.json").exists()
        has_spec = (grading_dir / "golden.spec.json").exists()
        
        # Priority: Run > State > Spec
        if has_run:
            stats["run"] += 1
        elif has_state:
            stats["state"] += 1
        elif has_spec:
            # Spec is now ILLEGAL in Training-Grade V2
            stats["spec"] += 1
            failures.append(f"Illegal Spec Artifact: {slug} (Must convert to Run/State)")
        else:
            stats["missing"] += 1
            missing_list.append(slug)
            
    if stats["missing"] > 0:
        print(f"[FAIL] {stats['missing']} quests missing golden artifacts completely.")
        failures.append(f"Missing Golden Artifacts: {stats['missing']} quests (e.g. {missing_list[0] if missing_list else ''})")

    # 3. Ratchet Check
    budget = load_budget()
    if budget:
        # max_spec should be 0, but if it exists in budget, we obey it (though we already failed above if spec > 0)
        if stats["spec"] > budget.get("max_spec", 0):
            failures.append(f"Ratchet Fail: Current SPEC ({stats['spec']}) > max_spec ({budget.get('max_spec', 0)})")
        if stats["run"] < budget.get("min_run", 0):
            failures.append(f"Ratchet Fail: Current RUN ({stats['run']}) < min_run ({budget['min_run']})")
        # Could also track min_state, but usually run/state are interchangeable "good" vs spec "blocked".
        # Total validated = run + state. 
    
    # 4. Drift Check
    print("\n[?] Checking for Drift...")
    drift_ok, drift_msg = run_drift_check()
    if not drift_ok:
        # drift_msg might contain unicode, safe print
        try:
             print(f"[FAIL] Drift Detected:\n{drift_msg}")
        except:
             print(f"[FAIL] Drift Detected (Generic Error)")
        failures.append("Drift Detected (Objectives != Golden State)")

    # REPORT
    print(f"\n{'='*40}")
    print("Certification Summary")
    print(f"Total Quests: {stats['total']}")
    print(f"  RUN   (High Fidelity) : {stats['run']}")
    print(f"  STATE (Fs/Git Check)  : {stats['state']}")
    print(f"  SPEC  (Blocked/Todo)  : {stats['spec']}")
    print(f"  MISSING               : {stats['missing']}")
    
    if budget:
         print(f"\nRatchet Status: {'PASS' if not any('Ratchet' in f for f in failures) else 'FAIL'}")
         print(f"  Budget: max_spec={budget.get('max_spec')}, min_run={budget.get('min_run')}")
    else:
         print("\nRatchet Status: N/A (No budget file)")

    if failures:
        print("\n[STOP] CERTIFICATION FAILED")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    else:
        print("\n[OK] CERTIFICATION PASSED")
        sys.exit(0)

if __name__ == "__main__":
    certify_training_grade()
