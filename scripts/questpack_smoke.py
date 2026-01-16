
import asyncio
import sys
import os
import json
import importlib

# Add root to pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Internal Service Imports
# Must set env vars first if needed
os.environ["EXECUTION_ENABLED"] = "1"
# Ensure we can import app modules
try:
    from arcade_app.services.runner_registry import RunnerRegistry
    from arcade_app.services.code_runner import run_code
    from arcade_app.services.quest_validate import validate_quest_attempt
    from arcade_app.models import QuestDefinition
except ImportError as e:
    print(f"❌ Failed to import internal services: {e}")
    sys.exit(1)

async def smoke_test_pack(file_path):
    print(f"\n🚬 Smoking Pack: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    all_pass = True

    for q in data:
        slug = q.get("slug")
        title = q.get("title")
        lang = q.get("language", "python")
        print(f"  🔹 Quest: {slug} ({lang})")

        # Mock Quest Definition for Validator
        # effectively explicitly typing dict to what validator expects (attr access? or dict access?)
        # validate_quest_attempt expects an object with attributes usually (SQLModel), 
        # but let's check implementation.
        # It uses getattr(quest_def, "objectives_json", ...).
        # So we need a class or object with these attributes.
        
        class MockQuest:
            def __init__(self, data):
                self.slug = data["slug"]
                self.language = data.get("language", "python")
                # Handle keys alias
                self.objectives_json = data.get("objectives_json") or data.get("objectives") or []
                self.tiered_hints_json = data.get("tiered_hints_json") or data.get("tiered_hints") or {}
                self.runtime_rules_json = data.get("runtime_rules_json") or data.get("runtime") or {}
                self.grading_json = data.get("grading") or {}
                self.workspace_json = data.get("workspace") or {}
        
        quest_def = MockQuest(q)
        smoke_cfg = q.get("smoke", {})
        
        # 1. Run Starter Code
        starter = q.get("starter_code", "")
        workspace_def = q.get("workspace")
        expect_pass = smoke_cfg.get("expect_starter_pass", False)
        
        print(f"    Running Starter ({'Expect PASS' if expect_pass else 'Expect FAIL'})...")
        res_starter = await internal_run_and_validate(starter, lang, quest_def, workspace=workspace_def)
        
        if res_starter["passed"] != expect_pass:
             print(f"    ❌ Starter outcome mismatch! Got Passed={res_starter['passed']}, Expected={expect_pass}")
             all_pass = False
        else:
             print(f"    ✅ Starter behavior correct.")

        # 2. Run Solution Code
        solution = smoke_cfg.get("solution_code")
        solution_files = smoke_cfg.get("solution_workspace_files")
        
        if solution or solution_files:
            print(f"    Running Solution (Expect PASS)...")
            
            # Merge workspace if needed
            run_workspace = None
            if workspace_def:
                import copy
                run_workspace = copy.deepcopy(workspace_def)
                if solution_files:
                    for sf in solution_files:
                        found = False
                        for f in run_workspace["files"]:
                            if f["path"] == sf["path"]:
                                f["content"] = sf["content"]
                                found = True
                                break
                        if not found:
                            run_workspace["files"].append(sf)
            
            res_sol = await internal_run_and_validate(solution, lang, quest_def, workspace=run_workspace)
            
            if not res_sol["passed"]:
                print(f"    ❌ Solution FAILED! Reasons: {[r['detail'] for r in res_sol['objective_results'] if not r['ok']]}")
                if res_sol.get("stderr"):
                    print(f"      Stderr: {res_sol['stderr'][:200]}...")
                all_pass = False
            else:
                print(f"    ✅ Solution PASSED.")
        else:
            print("    ⚠️ No solution_code provided in smoke config.")

    return all_pass

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

    # 2. Validate
    results = validate_quest_attempt(
        code=code or "", # Legacy code might be None
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
        "stderr": stderr
    }

if __name__ == "__main__":
    import argparse
    import glob
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="File or directory of questpacks")
    args = parser.parse_args()
    
    target_files = []
    if os.path.isdir(args.path):
        target_files = glob.glob(os.path.join(args.path, "*.json"))
    else:
        target_files = [args.path]
        
    print(f"Found {len(target_files)} file(s) to smoke test.")
    
    success = True
    for f in target_files:
        if not asyncio.run(smoke_test_pack(f)):
            success = False
            
    if not success:
        sys.exit(1)
        
    print("\n✅ All smoke tests passed.")
