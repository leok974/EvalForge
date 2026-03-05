import sys
import os
import json
import asyncio
from pathlib import Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from scripts.utils_questpacks import get_all_quest_slugs

DOCS_DIR = Path("docs")
AUDITS_DIR = DOCS_DIR / "audits"
REPORT_MD_PATH = AUDITS_DIR / "DEBT_BREAKDOWN.md"
REPORT_JSON_PATH = AUDITS_DIR / "DEBT_BREAKDOWN.json"
QUESTS_DIR = Path("data/quests")

async def generate_breakdown():
    print("🔍 Auditing Quest Debt Breakdown...\n")
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load active curriculum to ignore blocking quests
    active_slugs = set()
    manifest_path = Path("data/seed/active_curriculum.json")
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            active_slugs = set(data.get("active_slugs", []))
            
    # 2. Get all referenced slugs everywhere
    referenced_slugs = get_all_quest_slugs()
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    breakdown = {
        "total_debt_quests": 0,
        "by_world": {},
        "by_missing_field": {
            "missing_briefing": 0,
            "missing_starter_code": 0,
            "missing_workspace_files": 0,
            "missing_objectives": 0,
            "missing_key_terms": 0
        },
        "by_source_category": {
            "has_folder": 0,
            "zombie": 0
        },
        "by_reference": {
            "referenced_in_questpack": 0,
            "not_referenced": 0
        },
        "quests": []
    }
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        for q in quests:
            if q.slug in active_slugs:
                continue # Skip blocking
                
            breakdown["total_debt_quests"] += 1
            world_id = q.world_id or "unknown"
            if world_id not in breakdown["by_world"]:
                breakdown["by_world"][world_id] = 0
            breakdown["by_world"][world_id] += 1
            
            # Fields
            has_briefing = bool(q.briefing_md and q.briefing_md.strip()) or bool(q.detailed_description and q.detailed_description.strip())
            has_starter = bool(q.starter_code and q.starter_code.strip())
            has_workspace = False
            if q.workspace_json and "files" in q.workspace_json:
                files = q.workspace_json["files"]
                if any(f.get("content", "").strip() or f.get("path") for f in files):
                    has_workspace = True
                    
            has_objectives = bool(q.objectives_json and len(q.objectives_json) > 0)
            
            is_tier_2 = "-t2-" in q.slug or "_t2_" in q.slug or "Tier 2" in q.title or "(T2)" in q.title
            has_key_terms = False
            if is_tier_2:
                has_key_terms = len(q.key_terms) >= 3 if q.key_terms else False
            else:
                has_key_terms = True # Not required
            
            issues = []
            if not has_briefing:
                breakdown["by_missing_field"]["missing_briefing"] += 1
                issues.append("briefing")
            if not has_starter and not has_workspace:
                breakdown["by_missing_field"]["missing_starter_code"] += 1
                breakdown["by_missing_field"]["missing_workspace_files"] += 1
                issues.append("starter/workspace")
            if not has_objectives:
                breakdown["by_missing_field"]["missing_objectives"] += 1
                issues.append("objectives")
            if not has_key_terms:
                breakdown["by_missing_field"]["missing_key_terms"] += 1
                issues.append("key_terms")
                
            # Disk / Pack presence
            # Also check old docs/quests path just in case
            disk_path = QUESTS_DIR / q.slug
            disk_path_old = DOCS_DIR / "quests" / q.slug
            has_folder = disk_path.exists() or disk_path_old.exists()
            is_referenced = q.slug in referenced_slugs
            
            is_zombie = not has_folder and not is_referenced
            
            if has_folder:
                breakdown["by_source_category"]["has_folder"] += 1
            if is_zombie:
                breakdown["by_source_category"]["zombie"] += 1
                
            if is_referenced:
                breakdown["by_reference"]["referenced_in_questpack"] += 1
            else:
                breakdown["by_reference"]["not_referenced"] += 1
                
            breakdown["quests"].append({
                "slug": q.slug,
                "world_id": world_id,
                "issues": issues,
                "has_folder": has_folder,
                "is_referenced": is_referenced,
                "is_zombie": is_zombie
            })

    # Write JSON
    with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(breakdown, f, indent=2)
        
    # Write MD
    md = [
        "# Debt Quests Breakdown",
        f"**Total Debt Quests**: {breakdown['total_debt_quests']}\n",
        "## Summary by World",
    ]
    for w, count in sorted(breakdown["by_world"].items(), key=lambda x: x[1], reverse=True):
        md.append(f"- **{w}**: {count}")
        
    md.extend([
        "\n## Summary by Missing Field",
        f"- Missing Briefing: {breakdown['by_missing_field']['missing_briefing']}",
        f"- Missing Starter/Workspace: {breakdown['by_missing_field']['missing_starter_code']}",
        f"- Missing Objectives: {breakdown['by_missing_field']['missing_objectives']}",
        f"- Missing Key Terms (Tier 2): {breakdown['by_missing_field']['missing_key_terms']}",
        "\n## Summary by Source Category",
        f"- Has folder on disk: {breakdown['by_source_category']['has_folder']}",
        f"- DB-only Zombie (No folder, not referenced): {breakdown['by_source_category']['zombie']}",
        "\n## Summary by Reference",
        f"- Referenced in Questpacks: {breakdown['by_reference']['referenced_in_questpack']}",
        f"- Not referenced anywhere: {breakdown['by_reference']['not_referenced']}",
        "\n## Zombie Quests (Candidates for Pruning)"
    ])
    
    for q in [q for q in breakdown["quests"] if q["is_zombie"]]:
        md.append(f"- `{q['slug']}` ({q['world_id']})")
        
    md.extend([
        "\n## On-Disk Quests (Candidates for Bulk Rehydration)"
    ])
    for q in [q for q in breakdown["quests"] if q["has_folder"]]:
         md.append(f"- `{q['slug']}` ({q['world_id']}) - Issues: {','.join(q['issues'])}")
         
    REPORT_MD_PATH.write_text("\n".join(md), encoding="utf-8")
    
    print(f"✅ Breakdown complete. Total debt: {breakdown['total_debt_quests']}")
    print(f"🧟 Zombies: {breakdown['by_source_category']['zombie']}")
    print(f"📂 On-Disk: {breakdown['by_source_category']['has_folder']}")
    print(f"JSON: {REPORT_JSON_PATH}")
    print(f"MD: {REPORT_MD_PATH}")

if __name__ == "__main__":
    asyncio.run(generate_breakdown())
