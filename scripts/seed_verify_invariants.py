#!/usr/bin/env python3
"""
Seed Invariant Verification Script

Enforces that all quests being seeded have required fields configured.
Run this before seeding to catch configuration errors early.
"""

import sys
from typing import List, Dict, Any

# Import quest definitions
from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES

# Allowlist for quests that intentionally have no objectives
# (Should be empty for production quests)
ALLOWLIST_NO_OBJECTIVES = [
    # Intentional exceptions only
]

def verify_quest_invariants(quest_data: Dict[str, Any]) -> List[str]:
    """
    Verify quest configuration invariants.
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    slug = quest_data.get('slug', 'UNKNOWN')
    
    # Invariant 1: Objectives required (unless allowlisted)
    if slug not in ALLOWLIST_NO_OBJECTIVES:
        objectives = quest_data.get('objectives_json', [])
        if not objectives or len(objectives) == 0:
            errors.append(
                f"❌ Quest '{slug}' has no objectives. "
                f"Add objectives_json or add to ALLOWLIST_NO_OBJECTIVES if intentional."
            )
    
    # Invariant 2: Objectives must have required fields
    objectives = quest_data.get('objectives_json', [])
    for idx, obj in enumerate(objectives):
        obj_id = obj.get('id', f'objective_{idx}')
        
        if not obj.get('kind'):
            errors.append(f"❌ Quest '{slug}', objective '{obj_id}': missing 'kind' field")
        
        if not obj.get('rule'):
            errors.append(f"❌ Quest '{slug}', objective '{obj_id}': missing 'rule' field")
        
        # Validate rule structure
        rule = obj.get('rule', {})
        if isinstance(rule, dict) and not rule.get('kind'):
            errors.append(f"❌ Quest '{slug}', objective '{obj_id}': rule missing 'kind'")
    
    # Invariant 3: starting_code_path should exist (warning only)
    # This would require filesystem access, skip for now
    
    return errors

def main():
    """Run verification on all quest definitions."""
    print("🔍 Verifying quest seed invariants...")
    print(f"   Checking {len(STANDARD_QUESTLINES)} quests\n")
    
    all_errors = []
    passed_count = 0
    
    for quest in STANDARD_QUESTLINES:
        slug = quest.get('slug', 'UNKNOWN')
        errors = verify_quest_invariants(quest)
        
        if errors:
            all_errors.extend(errors)
            for error in errors:
                print(error)
        else:
            passed_count += 1
            print(f"✅ Quest '{slug}' passed all checks")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed_count} passed, {len(all_errors)} errors")
    print(f"{'='*60}\n")
    
    if all_errors:
        print("❌ SEED VALIDATION FAILED")
        print("Fix the errors above before seeding quests.")
        sys.exit(1)
    else:
        print("✅ ALL QUESTS PASSED VALIDATION")
        print("Safe to proceed with seeding.")
        sys.exit(0)

if __name__ == "__main__":
    main()
