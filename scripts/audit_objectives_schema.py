#!/usr/bin/env python3
"""
Audit all quest objectives for schema validity.

Checks:
1. Every objective has id, kind, rule
2. kind is in VALIDATORS registry
3. rule has required fields for that kind
4. No legacy obj_default objectives

Outputs:
- docs/audits/OBJECTIVES_SCHEMA_AUDIT.md
- docs/audits/OBJECTIVES_SCHEMA_AUDIT.json

Exit codes:
- 0: All valid
- 1: Invalid objectives found
"""

import sys
import os
import json
from datetime import datetime
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

def audit_objective(obj: dict, quest_slug: str) -> list[str]:
    """Return list of validation errors for this objective."""
    errors = []
    
    # Required fields
    if not obj.get('id'):
        errors.append("Missing 'id'")
    
    obj_id = obj.get('id', 'unknown')
    
    # Check for legacy obj_default pattern
    if obj_id == "obj_default" and not obj.get('kind'):
        errors.append("Legacy obj_default objective (missing 'kind')")
    
    if not obj.get('kind'):
        errors.append("Missing 'kind'")
        return errors  # Can't validate further
    
    if 'rule' not in obj:  # Allow empty rule dict
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
    
    return errors

def audit_all_quests():
    """Audit all quests and return report."""
    report = {
        "audit_date": datetime.now().isoformat(),
        "total_quests": 0,
        "total_objectives": 0,
        "invalid_quests": [],
        "quests_with_no_objectives": [],
        "valid_quests": 0,
        "summary": {}
    }
    
    # STANDARD_QUESTLINES is a flat list of quest dicts
    for quest in STANDARD_QUESTLINES:
        quest_slug = quest.get("slug", "unknown")
        world_id = quest.get("world_id", "unknown")
        report["total_quests"] += 1
        
        objectives = quest.get("objectives_json")
        
        # Check for missing/empty objectives
        if objectives is None or (isinstance(objectives, list) and len(objectives) == 0):
            if quest_slug not in ALLOWLIST_NO_OBJECTIVES:
                report["quests_with_no_objectives"].append({
                    "slug": quest_slug,
                    "world": world_id,
                    "reason": "objectives_json is missing or empty"
                })
            continue
        
        if not isinstance(objectives, list):
            report["invalid_quests"].append({
                "slug": quest_slug,
                "world": world_id,
                "errors": [{
                    "objective_id": "N/A",
                    "errors": [f"objectives_json must be a list, got {type(objectives).__name__}"],
                    "objective": str(objectives)[:100]
                }]
            })
            continue
        
        # Audit each objective
        quest_errors = []
        for idx, obj in enumerate(objectives):
            report["total_objectives"] += 1
            
            if not isinstance(obj, dict):
                quest_errors.append({
                    "objective_id": f"index_{idx}",
                    "errors": [f"Objective must be a dict, got {type(obj).__name__}"],
                    "objective": str(obj)[:100]
                })
                continue
            
            obj_errors = audit_objective(obj, quest_slug)
            if obj_errors:
                quest_errors.append({
                    "objective_id": obj.get("id", f"index_{idx}"),
                    "errors": obj_errors,
                    "objective": obj
                })
        
        if quest_errors:
            report["invalid_quests"].append({
                "slug": quest_slug,
                "world": world_id,
                "errors": quest_errors
            })
        else:
            report["valid_quests"] += 1
    
    # Summary
    report["summary"] = {
        "total_quests": report["total_quests"],
        "valid_quests": report["valid_quests"],
        "invalid_quests_count": len(report["invalid_quests"]),
        "quests_with_no_objectives_count": len(report["quests_with_no_objectives"]),
        "status": "PASS" if (not report["invalid_quests"] and not report["quests_with_no_objectives"]) else "FAIL"
    }
    
    return report

def generate_markdown_report(report: dict) -> str:
    """Generate markdown audit report."""
    status_emoji = "✅" if report["summary"]["status"] == "PASS" else "❌"
    
    md = f"""# Objectives Schema Audit Report

**Date:** {report['audit_date']}  
**Status:** {status_emoji} {report['summary']['status']}

## Summary

- **Total Quests Scanned:** {report['total_quests']}
- **Total Objectives:** {report['total_objectives']}
- **Valid Quests:** {report['valid_quests']}
- **Invalid Quests:** {report['summary']['invalid_quests_count']}
- **Quests with No Objectives:** {report['summary']['quests_with_no_objectives_count']}

---

"""
    
    if report['summary']['status'] == "PASS":
        md += "## ✅ All Quests Valid!\n\nNo issues found. All objectives have proper kind+rule schema.\n"
    else:
        # Quests with no objectives
        if report['quests_with_no_objectives']:
            md += f"## ⚠️  Quests with No Objectives ({len(report['quests_with_no_objectives'])})\n\n"
            for quest in report['quests_with_no_objectives']:
                md += f"- **{quest['slug']}** (World: {quest['world']})\n"
                md += f"  - {quest['reason']}\n\n"
        
        # Invalid quests
        if report['invalid_quests']:
            md += f"## ❌ Invalid Quests ({len(report['invalid_quests'])})\n\n"
            for quest in report['invalid_quests']:
                md += f"### {quest['slug']} (World: {quest['world']})\n\n"
                for error_group in quest['errors']:
                    md += f"**Objective:** `{error_group['objective_id']}`\n\n"
                    md += "**Errors:**\n"
                    for err in error_group['errors']:
                        md += f"- {err}\n"
                    md += f"\n**Raw Objective:**\n```json\n{json.dumps(error_group['objective'], indent=2)}\n```\n\n"
    
    md += f"""---

## Validator Registry

**Supported Objective Kinds:**

{', '.join(f'`{k}`' for k in sorted(VALIDATORS.keys()))}

## Per-Kind Rule Requirements

| Kind | Required Fields |
|------|----------------|
"""
    
    for kind in sorted(VALIDATORS.keys()):
        required = RULE_REQUIREMENTS.get(kind, [])
        req_str = ', '.join(f'`{r}`' for r in required) if required else "(none)"
        md += f"| `{kind}` | {req_str} |\n"
    
    return md

if __name__ == "__main__":
    print("🔍 Auditing quest objectives...")
    
    # Ensure audit directory exists
    Path("docs/audits").mkdir(parents=True, exist_ok=True)
    
    # Run audit
    report = audit_all_quests()
    
    # Generate JSON
    json_path = "docs/audits/OBJECTIVES_SCHEMA_AUDIT.json"
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"📄 JSON report: {json_path}")
    
    # Generate Markdown
    md = generate_markdown_report(report)
    md_path = "docs/audits/OBJECTIVES_SCHEMA_AUDIT.md"
    with open(md_path, "w", encoding='utf-8') as f:
        f.write(md)
    print(f"📄 Markdown report: {md_path}")
    
    # Print summary
    print(f"\n{'-'*60}")
    print(f"Status: {report['summary']['status']}")
    print(f"Valid: {report['valid_quests']}/{report['total_quests']} quests")
    print(f"Invalid: {report['summary']['invalid_quests_count']}")
    print(f"No Objectives: {report['summary']['quests_with_no_objectives_count']}")
    print(f"{'-'*60}")
    
    # Exit code
    has_errors = report['summary']['status'] == "FAIL"
    sys.exit(1 if has_errors else 0)
