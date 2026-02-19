import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_validate import VALIDATORS, RULE_REQUIREMENTS
from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES
from scripts.utils_questpacks import get_all_quest_slugs

ALLOWLIST = [
    # Quests explicitly allowed to have no objectives
    "sandbox-python",
    "playground-sql",
]

def load_quest_definition(slug: str) -> Dict[str, Any]:
    """
    Load quest definition from various sources.
    Priority:
    1. Seed Config (STANDARD_QUESTLINES)
    2. docs/quests/<slug>/quest.json
    3. data/quests/<slug>/quest.json
    """
    # 1. Check Seed Config
    for q in STANDARD_QUESTLINES:
        if q.get("slug") == slug:
            return q
    
    # 2. Check docs/quests
    docs_path = Path(f"docs/quests/{slug}/quest.json")
    if docs_path.exists():
        try:
            with open(docs_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading {docs_path}: {e}")
            
    # 3. Check data/quests
    data_path = Path(f"data/quests/{slug}/quest.json")
    if data_path.exists():
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading {data_path}: {e}")

    # Not found
    return None

def audit_objective(obj: dict, quest_slug: str) -> list[str]:
    """Return list of validation errors for this objective."""
    from arcade_app.services.quest_validate import audit_objective_schema
    return audit_objective_schema(obj)

def audit_all_quests():
    """Audit all quests and return report."""
    report = {
        "total_quests": 0,
        "total_objectives": 0,
        "invalid_quests": [],
        "quests_with_no_objectives": [],
        "quests_missing_definition": [],
        "valid_quests": 0,
    }
    
    all_slugs = sorted(list(get_all_quest_slugs()))
    
    for slug in all_slugs:
        report["total_quests"] += 1
        quest = load_quest_definition(slug)
        
        if not quest:
            report["quests_missing_definition"].append(slug)
            continue
            
        # Get objectives from either key
        objectives = quest.get("objectives_json") or quest.get("objectives", [])
        
        # Check for empty objectives
        if not objectives:
            if slug not in ALLOWLIST:
                report["quests_with_no_objectives"].append(slug)
            continue
        
        # Audit each objective
        quest_errors = []
        for obj in objectives:
            report["total_objectives"] += 1
            obj_errors = audit_objective(obj, slug)
            if obj_errors:
                quest_errors.append({
                    "objective_id": obj.get("id", "unknown"),
                    "errors": obj_errors,
                    "objective": obj
                })
        
        if quest_errors:
            report["invalid_quests"].append({
                "slug": slug,
                "errors": quest_errors
            })
        else:
            report["valid_quests"] += 1
    
    return report

if __name__ == "__main__":
    print("🔍 Auditing quest objectives (Full World)...")
    report = audit_all_quests()
    
    # Generate JSON
    Path("docs/audits").mkdir(parents=True, exist_ok=True)
    with open("docs/audits/OBJECTIVES_SCHEMA_AUDIT.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Generate Markdown output
    print(f"Checked {report['total_quests']} quests.")
    print(f"Valid: {report['valid_quests']}")
    print(f"Invalid: {len(report['invalid_quests'])}")
    print(f"Missing Def: {len(report['quests_missing_definition'])}")
    print(f"No Objectives: {len(report['quests_with_no_objectives'])}")
    
    if report['invalid_quests']:
        print("\n❌ Invalid Quests Example:")
        ex = report['invalid_quests'][0]
        # Adjust access based on report structure: list of {slug, errors: [{objective_id, errors: []}]}
        # The printing logic above had a bug: ex['errors'][0]['errors'] (list of strings)
        print(f"  {ex['slug']}: {ex['errors'][0]['errors']}")
        sys.exit(1)
        
    if report['quests_missing_definition']:
        print(f"\n⚠️  [WARN] {len(report['quests_missing_definition'])} quests missing definition (Skipped).")

    sys.exit(0)
