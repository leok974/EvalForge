#!/usr/bin/env python3
"""
Seed-time enforcement for objective schema validity.

This script validates quest objectives BEFORE they are seeded into the database.
It is the hard gate that prevents regressions.

Enforces:
1. All quests have objectives (unless allowlisted)
2. Every objective has id, kind, rule
3. kind is in VALIDATORS registry
4. rule has required fields for that kind
5. No legacy obj_default objectives

Usage:
    python scripts/seed_verify_invariants.py

Exit codes:
    0: All valid
    1: Violations found (seeding should be aborted)
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_validate import VALIDATORS, RULE_REQUIREMENTS
from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES

# Quests allowed to have no objectives (sandboxes, playgrounds)
ALLOWLIST_NO_OBJECTIVES = [
    "sandbox-python",
    "sandbox-sql",
    "sandbox-ts",
    "playground-python",
]

def validate_objective(obj: dict, quest_slug: str) -> list[str]:
    """Return list of validation errors for this objective."""
    errors = []
    
    # Required fields
    if not obj.get('id'):
        errors.append("Missing 'id'")
    
    obj_id = obj.get('id', 'unknown')
    
    # Check for legacy obj_default pattern
    if obj_id == "obj_default" and not obj.get('kind'):
        errors.append("❌ REGRESSION: Legacy obj_default objective detected (missing 'kind')")
    
    if not obj.get('kind'):
        errors.append("Missing 'kind'")
        return errors  # Can't validate further
    
    if 'rule' not in obj:
        errors.append("Missing 'rule'")
        return errors
    
    # Check kind is valid
    kind = obj['kind']
    if kind not in VALIDATORS:
        errors.append(f"Unknown kind '{kind}' (not in VALIDATORS registry)")
        supported = ', '.join(sorted(VALIDATORS.keys()))
        errors.append(f"  Supported kinds: {supported}")
        return errors
    
    # Check rule has required fields
    rule = obj['rule']
    if not isinstance(rule, dict):
        errors.append(f"Rule must be a dict, got {type(rule).__name__}")
        return errors
    
    required = RULE_REQUIREMENTS.get(kind, [])
    
    # Special case: AST requires at least one of the sub-rules
    if kind == "ast":
        has_ast_check = any(
            k in rule for k in 
            ['must_define_function', 'must_assign_variable', 'must_import', 'forbid_import']
        )
        if not has_ast_check:
            errors.append(
                "AST rule missing required check. "
                "Must have one of: must_define_function, must_assign_variable, must_import, forbid_import"
            )
    else:
        # Standard required fields
        for field in required:
            if field not in rule:
                errors.append(f"Rule missing required field '{field}' for kind '{kind}'")
    
    # Special validation: stdout_exact should use 'expected' not 'pattern'
    if kind == "stdout_exact" and 'pattern' in rule and 'expected' not in rule:
        errors.append("⚠️  stdout_exact should use 'expected' not 'pattern' (backward compat supported but deprecated)")
    
    return errors

def verify_all_quests() -> dict:
    """Verify all quests and return report."""
    violations = []
    total_quests = len(STANDARD_QUESTLINES)
    total_objectives = 0
    
    for quest in STANDARD_QUESTLINES:
        quest_slug = quest.get("slug", "unknown")
        world_id = quest.get("world_id", "unknown")
        
        objectives = quest.get("objectives_json")
        
        # Check for missing/empty objectives
        if objectives is None or (isinstance(objectives, list) and len(objectives) == 0):
            if quest_slug not in ALLOWLIST_NO_OBJECTIVES:
                violations.append({
                    "quest": quest_slug,
                    "world": world_id,
                    "errors": ["❌ FATAL: Quest has no objectives (not allowlisted)"]
                })
            continue
        
        if not isinstance(objectives, list):
            violations.append({
                "quest": quest_slug,
                "world": world_id,
                "errors": [f"❌ FATAL: objectives_json must be a list, got {type(objectives).__name__}"]
            })
            continue
        
        # Validate each objective
        quest_errors = []
        for idx, obj in enumerate(objectives):
            total_objectives += 1
            
            if not isinstance(obj, dict):
                quest_errors.append(f"Objective index {idx}: must be a dict, got {type(obj).__name__}")
                continue
            
            obj_errors = validate_objective(obj, quest_slug)
            if obj_errors:
                obj_id = obj.get('id', f'index_{idx}')
                for err in obj_errors:
                    quest_errors.append(f"Objective '{obj_id}': {err}")
        
        if quest_errors:
            violations.append({
                "quest": quest_slug,
                "world": world_id,
                "errors": quest_errors
            })
    
    return {
        "total_quests": total_quests,
        "total_objectives": total_objectives,
        "violations": violations,
        "status": "PASS" if not violations else "FAIL"
    }

if __name__ == "__main__":
    print("🔒 Verifying quest objectives schema invariants...")
    print()
    
    report = verify_all_quests()
    
    print(f"📊 Stats:")
    print(f"  - Total quests: {report['total_quests']}")
    print(f"  - Total objectives: {report['total_objectives']}")
    print(f"  - Violations: {len(report['violations'])}")
    print()
    
    if report['status'] == "PASS":
        print("✅ PASS - All quest objectives valid!")
        print("   Safe to seed to database.")
        sys.exit(0)
    else:
        print("❌ FAIL - Quest objective violations detected!")
        print()
        print("🚫 SEEDING ABORTED - Fix the following issues:")
        print()
        
        for violation in report['violations']:
            print(f"Quest: {violation['quest']} (World: {violation['world']})")
            for error in violation['errors']:
                print(f"  - {error}")
            print()
        
        print(f"Total violations: {len(report['violations'])} quests")
        print()
        print("Fix these issues before seeding to database.")
        sys.exit(1)
