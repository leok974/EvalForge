#!/usr/bin/env python3
"""
regenerate_snapshot.py — Re-sync TRAINING_GRADE_SNAPSHOT.json with current results.

Reads FINAL_SWEEP_VERIFICATION.json (produced by verify_all_modern_worlds.py) and
updates the verification_summary block in the snapshot to match exactly.

Usage:
    python scripts/regenerate_snapshot.py             # use existing verify output
    python scripts/regenerate_snapshot.py --run-verify  # run verify first, then sync

Exit codes:
    0 — snapshot up-to-date (no write needed) or successfully updated
    1 — error
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT          = Path(__file__).parent.parent
SNAPSHOT_PATH = ROOT / "docs/audits/TRAINING_GRADE_SNAPSHOT.json"
VERIFY_OUTPUT = ROOT / "docs/audits/FINAL_SWEEP_VERIFICATION.json"
VERIFY_SCRIPT = ROOT / "scripts/verify_all_modern_worlds.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def run_verify() -> None:
    print("[regenerate] Running verify_all_modern_worlds.py ...")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(VERIFY_SCRIPT)],
        encoding="utf-8", errors="replace",
    )
    if result.returncode not in (0, 1):
        print(
            f"[ERROR] verify_all_modern_worlds.py exited with {result.returncode}",
            file=sys.stderr,
        )
        sys.exit(1)
    print("[regenerate] Verify complete.\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    run_verify_flag = "--run-verify" in sys.argv

    if run_verify_flag:
        run_verify()

    # Validate inputs exist
    for p, label in [(VERIFY_OUTPUT, "FINAL_SWEEP_VERIFICATION.json"),
                     (SNAPSHOT_PATH, "TRAINING_GRADE_SNAPSHOT.json")]:
        if not p.exists():
            print(f"[ERROR] {label} not found at {p}", file=sys.stderr)
            if not run_verify_flag and p == VERIFY_OUTPUT:
                print("       Run with --run-verify, or run verify_all_modern_worlds.py first.",
                      file=sys.stderr)
            sys.exit(1)

    current_results = load_json(VERIFY_OUTPUT)
    snapshot        = load_json(SNAPSHOT_PATH)

    # ---- build new verification_summary from current run ----
    current_map: dict[str, dict] = {
        f"{r['pack']}:{r['mode']}": r for r in current_results
    }

    pack_names = sorted({key.rsplit(":", 1)[0] for key in current_map})
    new_summary: dict[str, dict] = {}

    for pack_name in pack_names:
        sol_key = f"{pack_name}:solution"
        stu_key = f"{pack_name}:student"

        sol_pass = (current_map[sol_key]["exit_code"] == 0) if sol_key in current_map else False
        stu_pass = (current_map[stu_key]["exit_code"] == 0) if stu_key in current_map else False

        # Preserve human-written notes from existing snapshot entries
        existing = snapshot.get("verification_summary", {}).get(pack_name, {})
        entry: dict = {"solution_pass": sol_pass, "student_pass": stu_pass}
        if "note" in existing:
            entry["note"] = existing["note"]

        new_summary[pack_name] = entry

    old_summary = snapshot.get("verification_summary", {})

    # ---- diff ----
    added   = sorted(set(new_summary) - set(old_summary))
    removed = sorted(set(old_summary) - set(new_summary))
    changed = sorted(
        k for k in new_summary
        if k in old_summary and new_summary[k] != old_summary[k]
    )

    if not added and not removed and not changed:
        print("[regenerate] Snapshot already up-to-date. No changes needed.")
        sys.exit(0)

    # ---- report diff ----
    if added:
        print(f"[+] Added ({len(added)}):")
        for k in added:
            print(f"    + {k}: {new_summary[k]}")
    if removed:
        print(f"[-] Removed ({len(removed)}):")
        for k in removed:
            print(f"    - {k}: {old_summary[k]}")
    if changed:
        print(f"[~] Changed ({len(changed)}):")
        for k in changed:
            print(f"    ~ {k}:")
            print(f"        before: {old_summary[k]}")
            print(f"        after:  {new_summary[k]}")

    # ---- write ----
    snapshot["verification_summary"] = new_summary
    snapshot.setdefault("metadata", {})["generated_at"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    save_json(SNAPSHOT_PATH, snapshot)
    print(f"\n[regenerate] Snapshot updated → {SNAPSHOT_PATH}")
    sys.exit(0)


if __name__ == "__main__":
    main()
