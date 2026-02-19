
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs
from arcade_app.services.quest_validate import VALIDATORS

def audit_phase_k():
    print("🔍 Auditing Phase K Queue (CLI/CSS/HTML/Node/React/SQL/Infra)...")
    
    all_slugs = get_all_quest_slugs()
    queue = []
    
    for slug in all_slugs:
        # Load quest definition FIRST (to check objectives)
        # Check docs/quests
        quest_data = None
        source = "unknown"
        json_path = Path(f"docs/quests/{slug}/quest.json")
        
        if json_path.exists():
            source = "docs/quests"
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    quest_data = json.load(f)
            except:
                pass
        
        # If not in docs, it might be in questpack (we can't easily check questpack JSON here without loading all packs)
        # But we can check if it's missing from docs, which implies it's either DB-only or embedded.
        # However, for Phase K, we want to materialize them in docs/quests if they don't exist?
        # Or update questpack if embedded.
        # Let's assume most are in questpacks if not in docs.
        
        # Check objectives status
        objs = quest_data.get("objectives", []) if quest_data else []
        
        has_issues = False
        issues = []
        
        if not objs:
            has_issues = True
            issues.append("No Objectives")
        else:
            # Check for legacy/invalid
            for o in objs:
                if o.get("id") == "obj_default" or not o.get("kind") or o.get("kind") not in VALIDATORS:
                    has_issues = True
                    issues.append("Invalid/Legacy Schema")
                    break
        
        # Check Golden
        grading_dir = Path(f"data/quests/{slug}/grading")
        has_run = (grading_dir / "golden.run.json").exists()
        has_state = (grading_dir / "golden.state.json").exists()
        has_spec = (grading_dir / "golden.spec.json").exists()
        
        if not (has_run or has_state):
             has_issues = True
             issues.append("Missing Golden (Run/State)")

        if has_issues:
            # Determine Metadata
            world = "unknown"
            if "node" in slug: world = "Node"
            elif "cli" in slug: world = "CLI"
            elif "html" in slug: world = "HTML"
            elif "css" in slug: world = "CSS"
            elif "react" in slug: world = "React"
            elif "sql" in slug: world = "SQL"
            elif "infra" in slug: world = "Infra"
            elif "docker" in slug: world = "Infra"
            
            # Check if tests exist
            workspace_dir = Path(f"data/quests/{slug}/workspace") # Or source
            # Actually, check logic:
            # 1. Does it have test files?
            has_tests = False
            # We can't easily check workspace without materializing.
            # But we can infer from slug or known patterns.
            
            rec_strategy = "Unknown"
            if world in ["Node", "React", "CLI"]:
                rec_strategy = "tests_pass (if tests exist) else stdout_regex"
            elif world in ["HTML", "CSS"]:
                rec_strategy = "fs_snapshot + source_regex/file_hash"
            elif world == "SQL":
                rec_strategy = "tests_pass (sql runner) or sql_exact"
            elif world == "Infra":
                rec_strategy = "golden.state + fs_snapshot"
                
            queue.append({
                "slug": slug,
                "world": world,
                "issues": ", ".join(issues),
                "golden": "RUN" if has_run else ("STATE" if has_state else ("SPEC" if has_spec else "NONE")),
                "strategy": rec_strategy
            })
            
    # Generate MD
    queue.sort(key=lambda x: (x["world"], x["slug"]))
    
    md = "# Phase K Backfill Queue\n\n"
    md += f"Found {len(queue)} quests needing attention.\n\n"
    md += "| World | Slug | Issues | Golden Status | Recommended Strategy |\n"
    md += "|---|---|---|---|---|\n"
    
    for q in queue:
        md += f"| **{q['world']}** | `{q['slug']}` | {q['issues']} | {q['golden']} | {q['strategy']} |\n"
        
    out_path = Path("docs/audits/PHASE_K_QUEUE.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    # Generate JSON Plan for Capture
    json_plan = []
    for q in queue:
        # Only include if missing or blocked spec
        json_plan.append({
            "slug": q["slug"],
            "world": q["world"],
            "strategy": q["strategy"]
        })
        
    json_path = Path("docs/audits/GOLDEN_ROLLOUT_PLAN_K.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_plan, f, indent=4)
        
    print(f"✅ Report generated: {out_path}")
    print(f"✅ Plan generated: {json_path}")
    print(f"Count: {len(queue)}")

if __name__ == "__main__":
    audit_phase_k()
