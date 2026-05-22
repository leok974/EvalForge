
import json
import sys
import subprocess
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
SNAPSHOT_PATH = ROOT_DIR / "docs/audits/TRAINING_GRADE_SNAPSHOT.json"
VERIFY_SCRIPT = ROOT_DIR / "scripts/verify_all_modern_worlds.py"
VERIFY_OUTPUT = ROOT_DIR / "docs/audits/FINAL_SWEEP_VERIFICATION.json"

def main():
    print("[CI] Starting CI Check: Training-Grade Guard")

    # 1. Run Verification (do not fail on non-zero exit — inactive-scope packs may fail)
    print(f"[CI] Running {VERIFY_SCRIPT.name}...")
    result = subprocess.run([sys.executable, "-X", "utf8", str(VERIFY_SCRIPT)])
    if result.returncode not in (0, 1):
        print(f"[CI] FAIL: Verification script crashed (exit {result.returncode}).")
        sys.exit(1)
    print(f"[CI] Verify completed (exit {result.returncode}). Checking snapshot packs only...")

    # 2. Load Snapshot and New Results
    if not SNAPSHOT_PATH.exists():
        print(f"[CI] FAIL: Snapshot not found at {SNAPSHOT_PATH}")
        sys.exit(1)

    if not VERIFY_OUTPUT.exists():
        print(f"[CI] FAIL: Verification output not found at {VERIFY_OUTPUT}")
        sys.exit(1)

    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    with open(VERIFY_OUTPUT, "r", encoding="utf-8") as f:
        current_results = json.load(f)

    # Map current results for easy lookup
    # key: "packname:mode" -> result dict
    current_map = {f"{r['pack']}:{r['mode']}": r for r in current_results}

    snapshot_summary = snapshot.get("verification_summary", {})

    failed = False

    print("\n[CI] Comparing against Snapshot...")

    for pack_name, baseline in snapshot_summary.items():
        # Check Solution Mode
        sol_key = f"{pack_name}:solution"
        if sol_key not in current_map:
            print(f"[MISSING] {sol_key} missing from current run.")
            failed = True
            continue

        sol_res = current_map[sol_key]
        sol_passed = (sol_res["exit_code"] == 0)
        expected_sol_pass = baseline.get("solution_pass", True)  # default True for backward compat

        if sol_passed != expected_sol_pass:
            if expected_sol_pass:
                print(f"[FAIL] {pack_name} (solution) failed! Expected PASS.")
                print(f"    Errors: {sol_res.get('result', {}).get('errors', 'Unknown')}")
            else:
                print(f"[DRIFT] {pack_name} (solution) PASSED but snapshot expects FAIL.")
            failed = True
        else:
            print(f"[PASS] {pack_name} (solution) - MATCHED SNAPSHOT ({'PASS' if sol_passed else 'FAIL'})")

        # Check Student Mode consistency
        stu_key = f"{pack_name}:student"
        if stu_key not in current_map:
            print(f"[MISSING] {stu_key} missing from current run.")
            failed = True
            continue

        stu_res = current_map[stu_key]
        stu_passed = (stu_res["exit_code"] == 0)
        expected_stu_pass = baseline["student_pass"]

        if stu_passed != expected_stu_pass:
            status_str = "PASSED" if stu_passed else "FAILED"
            expected_str = "PASS" if expected_stu_pass else "FAIL"
            print(f"[DRIFT] {pack_name} (student) {status_str} but expected {expected_str}.")
            failed = True
        else:
            print(f"[PASS] {pack_name} (student) - MATCHED SNAPSHOT ({'PASS' if stu_passed else 'FAIL'})")

    if failed:
        print("\n[CI] FAIL: Regressions or Drift detected.")
        sys.exit(1)

    # 3. Audit skipped e2e tests for overdue Revisit targets
    print("\n[CI] Auditing skipped tests...")
    audit_script = ROOT_DIR / "scripts" / "audit_skipped_tests.py"
    audit_result = subprocess.run([sys.executable, str(audit_script)])
    if audit_result.returncode != 0:
        print("[CI] FAIL: Overdue test.skip blocks detected.")
        sys.exit(1)

    print("\n[CI] PASS: System is Training-Grade Stable.")
    sys.exit(0)

if __name__ == "__main__":
    main()
