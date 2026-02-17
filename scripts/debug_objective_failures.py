#!/usr/bin/env python3
"""
Debug Objective Failures - Smoke Test Runner (Phase 6).

This script verifies that the validator engine produces HIGH QUALITY, ACTIONABLE error messages.
It runs each validator kind with a known-bad input and prints the resulting error object.

We check for:
1. ok=False
2. detail is helpful
3. expected/actual/diff fields are populated (where applicable)

Usage:
    python scripts/debug_objective_failures.py
"""

import sys
import os
from types import SimpleNamespace

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_validate import validate_quest_attempt

def make_quest_def(objectives):
    return SimpleNamespace(
        objectives_json=objectives,
        runtime_rules_json={"enabled": False},
        grading_json={},
        tier=0
    )

TEST_CASES = [
    {
        "kind": "stdout_exact",
        "desc": "Output Mismatch",
        "rule": {"expected": "Hello World"},
        "input": {"stdout": "Hello Python"},
        "checks": ["expected: Hello World", "actual: Hello Python", "diff: Expected:"]
    },
    {
        "kind": "stdout_regex",
        "desc": "Regex Mismatch",
        "rule": {"pattern": r"Item \d+", "description": "Item with number"},
        "input": {"stdout": "Item One"},
        "checks": ["expected: Item with number", "actual: Item One"]
    },
    {
        "kind": "source_regex",
        "desc": "Missing Source Pattern",
        "rule": {"pattern": r"def\s+main\(\):"},
        "input": {"code": "def foo(): pass"},
        "checks": ["detail: Source code missing required pattern"]
    },
    {
        "kind": "ast",
        "desc": "Missing Function",
        "rule": {"must_define_function": "calculate_total"},
        "input": {"code": "def other_func(): pass"},
        "checks": ["detail: Define function 'calculate_total'"]
    },
    {
        "kind": "ast",
        "desc": "Missing Variable",
        "rule": {"must_assign_variable": "score"},
        "input": {"code": "points = 10"},
        "checks": ["expected: Variable 'score' must be assigned", "diff: Expected:"]
    },
    {
        "kind": "json_output",
        "desc": "JSON Mismatch",
        "rule": {"expected": {"status": "ok"}},
        "input": {"stdout": '{"status": "error"}'},
        "checks": ["detail: JSON output mismatch"]
    },
    {
        "kind": "exit_code_zero",
        "desc": "Non-Zero Exit Code",
        "rule": {},
        "input": {"exit_code": 1},
        "checks": ["detail: Exit code 0", "ok: False"]
    },
    {
        "kind": "exit_code",
        "desc": "Wrong Exit Code",
        "rule": {"expected": 1},
        "input": {"exit_code": 0},
        "checks": ["expected: Exit code 1", "actual: Exit code 0"]
    }
]

def run_failure_smoke_test():
    print("🔥 Running Objective Failure Smoke Tests...\n")
    print(f"{'KIND':<20} | {'DESCRIPTION':<25} | {'STATUS':<10} | {'FEEDBACK QUALITY'}")
    print("-" * 100)
    
    passed = 0
    total = len(TEST_CASES)
    
    for case in TEST_CASES:
        kind = case["kind"]
        desc = case["desc"]
        
        obj = {
            "id": f"test_{kind}",
            "kind": kind,
            "rule": case["rule"]
        }
        
        inp = case["input"]
        res_list = validate_quest_attempt(
            code=inp.get("code", ""),
            stdout=inp.get("stdout", ""),
            stderr=inp.get("stderr", ""),
            exit_code=inp.get("exit_code", 0),
            quest_def=make_quest_def([obj])
        )
        
        res = res_list[0]
        
        # Verify failure
        if res["ok"]:
            print(f"{kind:<20} | {desc:<25} | ❌ FAILED  | Expected validation failure, got success")
            continue
            
        # Verify checks
        failure_msg = []
        checks_ok = True
        
        # Stringify result for checking
        res_str = str(res)
        
        for check in case["checks"]:
            # Simple substring check in str(res) representation or specific fields
            key, val = check.split(": ", 1) if ": " in check else (None, None)
            
            if key and key in res:
                if val not in str(res[key]):
                     failure_msg.append(f"Missing '{val}' in '{key}'")
                     checks_ok = False
            elif check not in res_str:
                failure_msg.append(f"Missing token '{check}'")
                checks_ok = False
        
        if checks_ok:
            print(f"{kind:<20} | {desc:<25} | ✅ PASS    | Verified: {', '.join(case['checks'])}")
            passed += 1
        else:
            print(f"{kind:<20} | {desc:<25} | ⚠️  WEAK    | {', '.join(failure_msg)}")
            print(f"   -> Result: {res}")
            
    print("-" * 100)
    print(f"\nResult: {passed}/{total} smoke tests passed quality check.")
    
    if passed == total:
        print("✅ All objective kinds produce actionable error messages!")
        sys.exit(0)
    else:
        print("❌ Some objective kinds need better error messages.")
        sys.exit(1)

if __name__ == "__main__":
    run_failure_smoke_test()
