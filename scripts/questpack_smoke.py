
import asyncio
import sys
import os
import json
import glob
from collections import defaultdict
import hashlib

# Add root to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Internal Service Imports
os.environ["EXECUTION_ENABLED"] = "1"
try:
    from arcade_app.services.runner_registry import RunnerRegistry
    from arcade_app.services.code_runner import run_code
    from arcade_app.services.quest_validate import validate_quest_attempt
    from arcade_app.models import QuestDefinition
except ImportError as e:
    print(f"❌ Failed to import internal services: {e}")
    sys.exit(1)

def find_json_files(root_dir):
    """Recursively find all .json files in relevant directories."""
    patterns = [
        os.path.join(root_dir, "data", "questpacks", "**", "*.json"),
        os.path.join(root_dir, "seed", "**", "*.json"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p, recursive=True))
    return sorted(list(set(files)))

class MockQuest:
    def __init__(self, data):
        self.slug = data.get("slug", "unknown")
        self.language = data.get("language", "python")
        self.id = data.get("id", self.slug)
        self.objectives_json = data.get("objectives_json") or data.get("objectives") or []
        self.tiered_hints_json = data.get("tiered_hints_json") or data.get("tiered_hints") or {}
        self.runtime_rules_json = data.get("runtime_rules_json") or data.get("runtime") or {}
        self.grading_json = data.get("grading") or {}
        self.workspace_json = data.get("workspace") or {}
        self.world_id = data.get("world_id", "unknown")
        self.track_id = data.get("track_id", "unknown")

async def internal_run_and_validate(code, language, quest_def, workspace=None):
    timeout = quest_def.runtime_rules_json.get("timeout_ms", 2000)
    mode = quest_def.grading_json.get("mode", "run")
    
    try:
        exec_res = run_code(language, code, timeout_ms=timeout, workspace=workspace, mode=mode)
        stdout = exec_res.stdout
        stderr = exec_res.stderr
        exit_code = exec_res.exit_code or 0
        timed_out = exec_res.timed_out
    except Exception as e:
        stdout = ""
        stderr = str(e)
        exit_code = 1
        timed_out = False

    results = validate_quest_attempt(
        code=code or "",
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        timed_out=timed_out,
        quest_def=quest_def
    )
    
    passed = all(r["ok"] for r in results) if results else True
    
    return {
        "passed": passed,
        "objective_results": results,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    }

def categorize_failure(res):
    if res["exit_code"] != 0 and res["stderr"]:
        if "Module not found" in res["stderr"] or "ImportError" in res["stderr"]:
            return "runtime_error_imports"
        return "runtime_error"
    if not res["objective_results"]:
         return "unknown_no_results"
    
    failed_objs = [r for r in res["objective_results"] if not r["ok"]]
    if not failed_objs:
        return "unknown_passed_but_marked_failed"
        
    kind = failed_objs[0].get("kind", "unknown")
    return f"objective_{kind}"

async def smoke_test_quest(q_data, debug_raw=False):
    quest_def = MockQuest(q_data)
    smoke_cfg = q_data.get("smoke", {})
    
    print(f"  🔹 Testing {quest_def.slug} ({quest_def.language})...")
    
    # Report Object
    report = {
        "quest_id": quest_def.id,
        "slug": quest_def.slug,
        "language": quest_def.language,
        "status": "PASS",
        "failures": []
    }

    # 1. Run Starter Code
    starter = q_data.get("starter_code", "")
    workspace_def = q_data.get("workspace")
    expect_starter_pass = smoke_cfg.get("expect_starter_pass", False)
    
    res_starter = await internal_run_and_validate(starter, quest_def.language, quest_def, workspace=workspace_def)
    
    if res_starter["passed"] != expect_starter_pass:
            print(f"    ❌ Starter outcome mismatch! Got Passed={res_starter['passed']}, Expected={expect_starter_pass}")
            report["status"] = "FAIL"
            report["failures"].append({
                "stage": "starter",
                "expected_pass": expect_starter_pass,
                "actual_pass": res_starter["passed"],
                "stdout": res_starter["stdout"],
                "stderr": res_starter["stderr"],
                "bucket": categorize_failure(res_starter)
            })
            
    # 2. Run Solution Code
    solution = smoke_cfg.get("solution_code")
    solution_files = smoke_cfg.get("solution_workspace_files")
    
    if solution or solution_files:
        run_workspace = None
        if workspace_def:
            import copy
            run_workspace = copy.deepcopy(workspace_def)
            if solution_files:
                for sf in solution_files:
                    found = False
                    # Make sure workspace["files"] is a list
                    if "files" not in run_workspace: run_workspace["files"] = []
                    
                    for f in run_workspace["files"]:
                        if f["path"] == sf["path"]:
                            f["content"] = sf["content"]
                            found = True
                            break
                    if not found:
                        run_workspace["files"].append(sf)
        
        # Calculate hash to detect changes later
        report["solution_hash"] = hashlib.md5((solution or "").encode('utf-8')).hexdigest()
        
        res_sol = await internal_run_and_validate(solution, quest_def.language, quest_def, workspace=run_workspace)
        
        if debug_raw:
            pass # Removed debug prints


        if not res_sol["passed"]:
            print(f"    ❌ Solution FAILED! Reasons: {[r['detail'] for r in res_sol['objective_results'] if not r['ok']]}")
            if res_sol.get("stderr"):
                print(f"      Stderr: {res_sol['stderr'][:200]}...")
            
            report["status"] = "FAIL"
            report["failures"].append({
                "stage": "solution",
                "stdout": res_sol["stdout"],
                "stderr": res_sol["stderr"],
                "objective_results": res_sol["objective_results"],
                "bucket": categorize_failure(res_sol)
            })
        else:
            print(f"    ✅ Solution PASSED.")
    else:
        print("    ⚠️ No solution_code provided in smoke config.")
        report["status"] = "SKIPPED_NO_SOLUTION"
        
    return report

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="File or directory of questpacks")
    parser.add_argument("--all", action="store_true", help="scan all")
    parser.add_argument("--root", default=os.getcwd(), help="Root dir")
    parser.add_argument("--only", help="Run only specific quest slug")
    parser.add_argument("--debug-raw", action="store_true", help="Print raw stdout/stderr")
    parser.add_argument("--debug", action="store_true", help="Alias for debug-raw")
    args = parser.parse_args()
    
    # Alias debug to debug_raw
    if args.debug:
        args.debug_raw = True
    
    target_files = []
    if args.all:
        target_files = find_json_files(args.root)
    elif args.path:
        if os.path.isdir(args.path):
            target_files = glob.glob(os.path.join(args.path, "*.json"))
        else:
            target_files = [args.path]
            
    print(f"Found {len(target_files)} file(s) to scan for smoke candidates.")
    
    all_quests = []
    for f in target_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, list): all_quests.extend(data)
            elif isinstance(data, dict):
                 if "packs" in data: all_quests.extend(data["packs"])
                 elif "quests" in data: all_quests.extend(data["quests"])
                 elif "slug" in data: all_quests.append(data)
        except Exception as e:
            print(f"Failed to load {f}: {e}")

    # Sample Quests (1 per track)
    grouped = defaultdict(lambda: defaultdict(list))
    for q in all_quests:
        w = q.get("world_id", "unknown")
        t = q.get("track_id", "unknown")
        grouped[w][t].append(q)
    if args.only:
        sampled = [q for q in all_quests if q.get("slug") == args.only]
        print(f"Filtered to single quest: {args.only}")
    else:
        # Pick 1 from each track
        sampled = []
        for w, tracks in grouped.items():
            for t, quests in tracks.items():
                # Prefer ones with smoke config
                candidates_with_smoke = [q for q in quests if "smoke" in q]
                if candidates_with_smoke:
                    sampled.append(candidates_with_smoke[0])
                elif quests:
                    # If no smoke config, maybe skip or try anyway? 
                    # User asked to "sample at least 1 quest per world/track".
                    # If no smoke config, we can't really test solution passing, but can test starter.
                    sampled.append(quests[0])
                
    print(f"Selected {len(sampled)} quests for smoke testing.")
    
    reports = []
    for q in sampled:
        reports.append(await smoke_test_quest(q, debug_raw=args.debug_raw))
            
    # Write Report
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/smoke-content-failures.json", "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)
        print("\n📄 Report written to artifacts/smoke-content-failures.json")

    # Generate Markdown Summary
    md_lines = ["# Smoke Test Failures Report", "", "| Slug | Language | Stage | Failure Bucket | Hint |", "|---|---|---|---|---|"]
    failed = [r for r in reports if r["status"] == "FAIL"]
    
    # Group by bucket for summary
    by_bucket = defaultdict(list)
    
    for r in failed:
        for f in r['failures']:
            bucket = f['bucket']
            hint = "Check logic"
            if bucket == "runtime_error_imports": hint = "Missing file/dependency"
            elif bucket == "unknown_passed_but_marked_failed": hint = "Starter code passed unexpectedly"
            elif bucket == "unknown_no_results": hint = "Zero tests found or runner crashed"
            
            md_lines.append(f"| `{r['slug']}` | {r['language']} | {f['stage']} | `{bucket}` | {hint} |")
            by_bucket[bucket].append(r['slug'])

    with open("artifacts/smoke-content-failures.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        print("📄 Markdown report written to artifacts/smoke-content-failures.md")

    # Summary
    if failed:
        print("\n🛑 FAILURES DETECTED:")
        for r in failed:
            print(f"  - {r['slug']} ({r['language']})")
            for f in r['failures']:
                print(f"    [{f['stage']}] {f['bucket']}")
        sys.exit(1)
        
    print("\n✅ All smoke tests passed.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
