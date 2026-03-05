import asyncio
import json
import sys
import os
from pathlib import Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition

async def lock_in_compliant_quests():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    compliant_slugs = []
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        for q in quests:
            issues = []
            
            # 1. Briefing
            has_briefing = bool(q.briefing_md and q.briefing_md.strip())
            has_detailed = bool(q.detailed_description and q.detailed_description.strip())
            if not has_briefing and not has_detailed:
                issues.append("briefing")
                
            # 2. Starter Code
            has_starter = bool(q.starter_code and q.starter_code.strip())
            has_workspace = False
            if q.workspace_json and "files" in q.workspace_json:
                files = q.workspace_json["files"]
                if any(f.get("content", "").strip() or f.get("path") for f in files):
                    has_workspace = True
            if not has_starter and not has_workspace:
                issues.append("starter")
                
            # 3. Objectives
            if not q.objectives_json or len(q.objectives_json) == 0:
                issues.append("objectives")
                
            # 4. Key Terms (Tier 2 only)
            is_tier_2 = "-t2-" in q.slug or "_t2_" in q.slug or "Tier 2" in q.title or "(T2)" in q.title
            if is_tier_2:
                terms_count = len(q.key_terms) if q.key_terms else 0
                if terms_count < 3:
                    issues.append("key_terms")
                    
            if not issues:
                compliant_slugs.append(q.slug)

    print(f"Found {len(compliant_slugs)} fully compliant quests. Locking them into active_curriculum.json.")
    
    manifest_path = Path("data/seed/active_curriculum.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"active_slugs": sorted(compliant_slugs)}, f, indent=2)

if __name__ == "__main__":
    asyncio.run(lock_in_compliant_quests())
