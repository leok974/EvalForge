#!/usr/bin/env python3
"""
scripts/audit_quest_validation_config.py

Audits quest definitions to ensure Tier-1 quests have valid, non-placeholder validation rules.
Fails if:
- Tier-1 quest has no objectives
- Objectives use placeholder content ("Complete the assignment", kind=TODO)
- stdout_regex objectives are missing patterns
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_QUESTPACK_DIR = Path("data/questpacks")

def check_quest(q: Dict[str, Any]) -> List[str]:
    errors = []
    slug = q.get("slug", "unknown")
    tier = q.get("tier", 0)
    
    # Only check Tier 1+
    if tier < 1:
        return []

    objectives = q.get("objectives_json", []) or q.get("objectives", [])
    
    if not objectives:
        # Check if it's explicitly a sandbox/demo with no checks?
        # Assuming all Tier-1 training quests need checks.
        errors.append("EF_OBJ_MISSING: No objectives configured.")
        return errors

    for i, obj in enumerate(objectives):
        title = str(obj.get("title", "")).lower()
        kind = str(obj.get("kind", "")).lower()
        rule = obj.get("rule", {}) # JSON field is 'rule' in logic, mapped from 'rule_json' in DB? 
        # In JSON files it's usually just "rule" or "rule_json". Let's support both.
        if "rule_json" in obj and not rule:
            rule = obj["rule_json"]

        # 1. Check Placeholders
        is_placeholder = False
        if "complete the assignment" in title: is_placeholder = True
        if kind in ["", "placeholder", "tbd", "todo"]: is_placeholder = True
        if not rule or rule == "TODO": is_placeholder = True

        if is_placeholder:
            errors.append(f"EF_OBJ_PLACEHOLDER: Objective #{i} '{title}' is a placeholder.")

        # 2. Check Specific Rules
        if kind == "stdout_regex":
            if not isinstance(rule, dict) or not rule.get("pattern"):
                errors.append(f"EF_INVALID_RULE: Objective #{i} '{title}' (stdout_regex) missing 'pattern'.")

    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", help="Filter by world ID")
    parser.add_argument("--fail-on-warn", action="store_true", help="Fail if any issues found")
    args = parser.parse_args()

    # Load Questpacks
    questpacks = sorted(DEFAULT_QUESTPACK_DIR.glob("*.json"))
    
    total_quests = 0
    total_errors = 0
    
    for qp_path in questpacks:
        try:
            data = json.loads(qp_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"❌ Failed to parse {qp_path}: {e}")
            total_errors += 1
            continue

        quests = []
        if isinstance(data, list):
            quests = data
        elif isinstance(data, dict):
             # Filter by world if requested (and if pack has it)
             if args.world:
                 # Pack level check
                 pack_world = data.get("world_id") or data.get("world")
                 if pack_world and pack_world != args.world:
                     continue
             quests = data.get("quests", [])

        for q in quests:
            # Filter by world (quest level)
            if args.world and q.get("world_id") != args.world:
                continue
                
            slug = q.get("slug")
            # Run Check
            errs = check_quest(q)
            
            if errs:
                print(f"\n❌ {slug} (Tier {q.get('tier')})")
                for e in errs:
                    print(f"   - {e}")
                total_errors += 1
            
            total_quests += 1

    print(f"\nChecked {total_quests} quests. Found issues in {total_errors} quests.")
    
    if args.fail_on_warn and total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
