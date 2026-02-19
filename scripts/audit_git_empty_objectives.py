import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs

def audit_git_empty():
    print("🔍 Auditing Git Empty Objectives...")
    
    all_slugs = get_all_quest_slugs()
    git_empty = []
    
    for slug in all_slugs:
        # Check source
        json_path = Path(f"docs/quests/{slug}/quest.json")
        source = "unknown"
        has_objectives = False
        obj_count = 0
        
        if json_path.exists():
            source = "docs/quests"
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    objs = data.get("objectives", [])
                    if objs:
                        has_objectives = True
                        obj_count = len(objs)
            except:
                pass
        
        # Check golden state
        grading_dir = Path(f"data/quests/{slug}/grading")
        has_golden_state = (grading_dir / "golden.state.json").exists()
        
        if not has_objectives:
            # Is it a git quest?
            if "git" in slug:
                git_empty.append({
                    "slug": slug,
                    "source": source,
                    "has_golden_state": has_golden_state,
                    "pack": "git_core" # Assumed for now
                })
                
    # Generate Report
    md = "# Phase J: Git Empty Objectives Audit\n\n"
    md += f"Found {len(git_empty)} Git quests with no/empty objectives.\n\n"
    md += "| Slug | Source | Has Golden State | Recommended Action |\n"
    md += "|---|---|---|---|\n"
    
    for q in git_empty:
        action = "Backfill from State" if q["has_golden_state"] else "Capture State & Backfill"
        md += f"| `{q['slug']}` | `{q['source']}` | {'✅' if q['has_golden_state'] else '❌'} | {action} |\n"
        
    out_path = Path("docs/audits/PHASE_J_GIT_EMPTY_OBJECTIVES.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    print(f"✅ Report generated: {out_path}")
    print(f"Count: {len(git_empty)}")

if __name__ == "__main__":
    audit_git_empty()
