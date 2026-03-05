#!/usr/bin/env python3
"""
CI Check Script - Run all critical audits and tests for objectives.

This script acts as the single source of truth for CI gates regarding quest objectives.
It runs:
1. Schema Audit (audit_objectives_schema.py)
2. Seed Invariants (seed_verify_invariants.py)
3. Golden Coverage (audit_golden_coverage.py)
4. Validator Smoke Tests (pytest tests/test_objective_validators.py)

Usage:
    python scripts/ci_check.py

Exit Code:
    0: All checks passed
    1: One or more checks failed
"""

import subprocess
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

STAGES = [
    {
        "name": "Schema Audit",
        "cmd": [sys.executable, "scripts/audit_objectives_schema.py"],
        "critical": True
    },
    {
        "name": "Objectives Shape Audit",
        "cmd": [sys.executable, "scripts/audit_objectives_shape.py"],
        "critical": True
    },
    {
        "name": "Objectives Serializer Shape Tests",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_objectives_serializer_shape.py", "-v"],
        "critical": True
    },
    {
        "name": "Seed Invariants",
        "cmd": [sys.executable, "scripts/seed_verify_invariants.py"],
        "critical": True
    },
    {
        "name": "Golden Coverage",
        "cmd": [sys.executable, "scripts/audit_golden_coverage.py"],
        "critical": True  # Now enforced
    },
    {
        "name": "Validator Smoke Tests",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_objective_validators.py"],
        "critical": True
    },
    {
        "name": "Seed Logic Tests",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_seed_validation.py"],
        "critical": True
    },
    {
        "name": "Seed Content Completeness Audit",
        "cmd": [sys.executable, "scripts/audit_seed_content_completeness.py"],
        "critical": True
    },
    {
        "name": "Runtime Fallback Tests",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_runtime_objectives_fallback.py"],
        "critical": True
    },
    {
        "name": "Drift & Parity Regression",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_drift_checks.py", "tests/test_seed_parity_regression.py"],
        "critical": True
    },
    {
        "name": "Schema Fuzzing",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_objective_schema_fuzz.py"],
        "critical": True
    },
    {
        "name": "Certified Worlds Smoke",
        "cmd": [sys.executable, "-m", "pytest", "tests/test_certified_worlds_smoke.py"],
        "critical": True
    },
    {
        "name": "Training Grade Certification",
        "cmd": [sys.executable, "scripts/certify_training_grade.py"],
        "critical": True
    }
]

def run_checks():
    print("🚀 Starting EvalForge CI Checks for Quest Objectives...\n")
    
    failed_critical = []
    failed_optional = []
    
    for stage in STAGES:
        name = stage["name"]
        cmd = stage["cmd"]
        critical = stage["critical"]
        
        print(f"▶️  Running {name}...")
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            # Run command and stream output
            result = subprocess.run(cmd, check=False)
            
            if result.returncode == 0:
                print(f"✅ {name} PASSED\n")
            else:
                if critical:
                    print(f"❌ {name} FAILED (Exit Code: {result.returncode})\n")
                    failed_critical.append(name)
                else:
                    print(f"⚠️  {name} FAILED (Optional/Warning) - Continuing...\n")
                    failed_optional.append(name)
                    
        except Exception as e:
            print(f"❌ Execution Error for {name}: {e}\n")
            if critical:
                failed_critical.append(name)
            else:
                failed_optional.append(name)

    print("-" * 60)
    print("📊 CI Check Summary")
    print("-" * 60)
    
    if failed_optional:
        print(f"⚠️  Warnings (Optional Checks Failed):")
        for name in failed_optional:
            print(f"   - {name}")
        print()
        
    if failed_critical:
        print(f"❌ CRITICAL FAILURES:")
        for name in failed_critical:
            print(f"   - {name}")
        print("\n🚫 CI Failed - Fix critical errors above.")
        sys.exit(1)
    
    print("✅ ALL CRITICAL CHECKS PASSED")
    sys.exit(0)

if __name__ == "__main__":
    run_checks()
