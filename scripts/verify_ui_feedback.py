import sys
import os
import json

# Adjust path to find arcade_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.services.quest_validate import validate_quest_attempt

# Mock Quest Definition
class MockQuest:
    def __init__(self):
        # Using dict approach if quest_def is checked as generic
        # or minimal attributes
        self.objectives_json = [
            {
                "id": "fs_snapshot", 
                "kind": "fs_snapshot", 
                "rule": {"must_exist": ["README.md", "main.py"], "must_not_exist": ["secret.txt"]}
            },
            {
                "id": "git_status_clean",
                "kind": "git_status_clean",
                "rule": {"expected_porcelain": ""}
            },
            {
                "id": "git_log_contains",
                "kind": "git_log_contains",
                "rule": {"must_contain": ["Initial commit"], "min_commits": 1}
            }
        ]
        self.grading_json = {}
        self.runtime_rules_json = {}
        self.slug = "mock-quest-verify"
        self.language = "python"
        
def run_verification():
    print("🚀 Verifying UI Feedback for State Failures")
    
    # Scene 1: Broken State (Missing file, Dirty git, Bad log)
    # Expected: 
    #   fs_snapshot FAIL: Missing README.md, Forbidden secret.txt
    #   git_status FAIL: Dirty
    #   git_log FAIL: Missing Initial commit
    
    # State Mock from ExecResult
    broken_state = {
        "files": ["main.py", "secret.txt"], # Missing README, Extra secret
        "git": {
            "has_dot_git": True,
            "status_porcelain": "M main.py", # Dirty
            "log_oneline": ["123456 Bad commit"], # Missing initial
            "branch": "master"
        },
        "hashes": {}
    }
    
    quest = MockQuest()
    
    # Call validate
    # Need to mimic how routes call it
    # validate_quest_attempt(code, stdout, stderr, exit_code, timed_out, quest_def, state)
    
    results = validate_quest_attempt(
        code="print('Hello')",
        stdout="Hello\n",
        stderr="",
        exit_code=0,
        timed_out=False,
        quest_def=quest,
        state=broken_state
    )
    
    print("\n--- Validation Results (Broken State) ---")
    # Simplify output for readability
    for r in results:
        print(f"[{'PASS' if r['ok'] else 'FAIL'}] {r['id']}: {r.get('detail', '')}")
        if not r['ok'] and r.get('diff'):
            print(f"  DIFF:\n{r['diff']}")
    
    # Verify Failure Count
    failures = [r for r in results if not r["ok"]]
    if len(failures) != 3:
        print(f"\n❌ Expected 3 failures, got {len(failures)}")
        sys.exit(1)
        
    # Check FS Snapshot detail
    fs_res = next(r for r in results if r["id"] == "fs_snapshot")
    # Check text content robustly
    detail = fs_res.get("detail", "")
    if "Missing" in detail and "README.md" in detail and "secret.txt" in detail:
        print("✅ FS Snapshot feedback is actionable.")
    else:
        print(f"❌ FS Snapshot feedback poor: {detail}")

    # Check Git Status detail
    git_res = next(r for r in results if r["id"] == "git_status_clean")
    diff = git_res.get("diff", "")
    if "Git status mismatch" in git_res["detail"] and "Actual Git Status" in diff:
        print("✅ Git Status feedback is actionable.")
    else:
        print(f"❌ Git Status feedback poor: {git_res.get('detail')} / {diff}")

if __name__ == "__main__":
    run_verification()
