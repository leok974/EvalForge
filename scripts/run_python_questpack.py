#!/usr/bin/env python3
"""
scripts/run_python_questpack.py

Executes and validates Python quests from a questpack JSON definition.
Acts as a CI gate to ensure quests are runnable and solvable (if solutions provided).

Usage:
  python scripts/run_python_questpack.py --questpack data/questpacks/python_systems.json --mode student
  python scripts/run_python_questpack.py --questpack data/questpacks/python_systems.json --mode solution
"""

import argparse
import json
import subprocess
import sys
import tempfile
import shutil
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Ensure we can import from arcade_app
sys.path.append(str(Path(__file__).parent.parent))

try:
    from arcade_app.services.quest_validate import validate_quest_attempt
except ImportError:
    print("Error: Could not import arcade_app.services.quest_validate.")
    print("Ensure you are running from the repo root or have set PYTHONPATH.")
    sys.exit(1)


@dataclass
class QuestResult:
    slug: str
    passed: bool
    details: List[Dict[str, Any]]
    stdout: str
    stderr: str


def run_quest(
    quest_def: Dict[str, Any],
    questpack_path: Path,
    mode: str = "student",
    solutions_root: Optional[Path] = None
) -> QuestResult:
    slug = quest_def["slug"]
    print(f"👉 Running {slug} [{mode}]...")

    # 1. Prepare Workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # A. Copy base workspace
        workspace_conf = quest_def.get("workspace", {})
        files_from = workspace_conf.get("files_from")
        
        if files_from:
            # Resolve relative to questpack
            source_path = (questpack_path.parent / files_from).resolve()
            if not source_path.exists():
                print(f"   ❌ ERROR: Workspace path not found: {source_path}")
                return QuestResult(slug, False, [{"error": f"Workspace path not found: {source_path}"}], "", "")
            
            shutil.copytree(source_path, temp_path, dirs_exist_ok=True)
        
        # B. Apply Solution Overlay (if mode=solution)
        if mode == "solution":
            if not solutions_root:
                 # Default to repo_root/solutions
                 solutions_root = Path(__file__).parent.parent / "solutions"
            
            sol_path = solutions_root / slug
            if sol_path.exists():
                print(f"   Overlaying solution from {sol_path}")
                shutil.copytree(sol_path, temp_path, dirs_exist_ok=True)
            else:
                print(f"   ⚠️ No solution found at {sol_path}, running as student/starter.")

        # 2. Run Entrypoint
        # Check grading_json for entrypoint, default to main.py
        grading = quest_def.get("grading_json", {})
        entrypoint = grading.get("entrypoint", quest_def.get("entrypoint", "main.py"))
        entry_file = temp_path / entrypoint
        
        if not entry_file.exists():
             print(f"   ❌ ERROR: Entrypoint {entrypoint} not found in workspace temp path {temp_path}")
             return QuestResult(slug, False, [{"error": f"Entrypoint {entrypoint} not found in workspace"}], "", "")

        # Timeout config
        runtime_rules = quest_def.get("runtime_rules_json", {})
        timeout_s = runtime_rules.get("timeout_ms", 2000) / 1000.0

        try:
            proc = subprocess.run(
                [sys.executable, entrypoint],
                cwd=temp_path,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                encoding="utf-8"  # Force utf-8
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
            timed_out = False
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = e.stderr or ""
            exit_code = -1
            timed_out = True
        except Exception as e:
            print(f"   ❌ SUBPROCESS FAILED: {e}")
            return QuestResult(slug, False, [{"error": f"Subprocess execution failed: {e}"}], "", "")

        # 3. Validate
        # Mock class for validator expectations
        class MockQuest:
            def __init__(self, d):
                objs = d.get("objectives_json") or d.get("objectives") or []
                # Normalize rule_json -> rule
                self.objectives_json = []
                for o in objs:
                    o_copy = o.copy()
                    if "rule_json" in o_copy and "rule" not in o_copy:
                        o_copy["rule"] = o_copy["rule_json"]
                    self.objectives_json.append(o_copy)
                    
                self.runtime_rules_json = d.get("runtime_rules_json", {})
                self.tier = d.get("tier", 1)

        try:
            validation_results = validate_quest_attempt(
                code="", # We don't analyze code in this script yet, just output
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                timed_out=timed_out,
                quest_def=MockQuest(quest_def)
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return QuestResult(slug, False, [{"error": f"Validator crashed: {e}", "traceback": traceback.format_exc()}], stdout, stderr)

        passed = all(r["ok"] for r in validation_results)
        
        # Print failure details immediately
        if not passed:
            print(f"   ❌ FAILED")
            print(f"      Exit Code: {exit_code}")
            if timed_out:
                print(f"      TIMED OUT")
            
            if not validation_results:
                print("      [WARNING] No validation results returned!")
            
            for r in validation_results:
                status = "OK" if r['ok'] else "FAIL"
                print(f"      - [{r['id']}] {status}: {r['detail']}")
            
            # Print stdout/stderr explicitly on failure
            if stdout:
                print("      --- STDOUT ---")
                print(stdout)
                print("      --------------")
            else:
                 print("      (stdout empty)")
                 
            if stderr:
                print("      --- STDERR ---")
                print(stderr)
                print("      --------------")
            else:
                 print("      (stderr empty)")
        else:
            print(f"   ✅ PASSED")

        return QuestResult(slug, passed, validation_results, stdout, stderr)


def main():
    parser = argparse.ArgumentParser(description="Run Python Questpack")
    parser.add_argument("--questpack", required=True, help="Path to questpack JSON")
    parser.add_argument("--only-slug", help="Run only specific quest slug")
    parser.add_argument("--mode", choices=["student", "solution"], default="student", help="Run mode")
    parser.add_argument("--solutions-dir", help="Custom solutions directory root")
    
    args = parser.parse_args()
    
    qp_path = Path(args.questpack)
    if not qp_path.exists():
        print(f"Questpack not found: {qp_path}")
        sys.exit(1)
        
    with open(qp_path, "r", encoding="utf-8") as f:
        quests = json.load(f)
        
    # Filter
    if args.only_slug:
        quests = [q for q in quests if q["slug"] == args.only_slug]
        
    if not quests:
        print("No quests to run.")
        sys.exit(0)

    print(f"=== Running {len(quests)} quests from {qp_path.name} in {args.mode} mode ===")
    
    failures = []
    
    for q in quests:
        res = run_quest(
            q, 
            qp_path, 
            mode=args.mode, 
            solutions_root=Path(args.solutions_dir) if args.solutions_dir else None
        )
        if not res.passed:
            failures.append(res)
            
    summary = {
        "total": len(quests),
        "passed": len(quests) - len(failures),
        "failed": len(failures),
        "errors": [f.stderr[-200:] if f.stderr else "" for f in failures], # snippet of errors
        "slugs": [{"slug": q["slug"], "status": "failed" if any(f.slug == q["slug"] for f in failures) else "passed"} for q in quests]
    }
    print(f"EF_RUNNER_RESULT_JSON={json.dumps(summary)}")

    print("\n" + "="*40)
    if failures:
        print(f"❌ FAILED: {len(failures)}/{len(quests)} quests failed.")
        sys.exit(1)
    else:
        print(f"✅ SUCCESS: {len(quests)} quests passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
