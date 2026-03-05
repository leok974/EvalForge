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

QUESTS_DIR = Path("data/quests")
DOCS_DIR = Path("docs")

async def fix_legacy_regex_objectives():
    print("🔧 Fixing legacy regex fields in objectives...")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    fixed_count = 0
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        for q in quests:
            if not q.objectives_json:
                continue
                
            needs_update = False
            new_obj = []
            
            for obj in q.objectives_json:
                if "rules" in obj:
                    for rule in obj["rules"]:
                        if rule.get("kind") in ("stdout_regex", "source_regex") or "regex" in rule.get("kind", ""):
                            if "regex" in rule and "pattern" not in rule:
                                rule["pattern"] = rule.pop("regex")
                                needs_update = True
                                
                new_obj.append(obj)
                
            if needs_update:
                q.objectives_json = new_obj
                # Now fix it on disk as well!
                disk_path = QUESTS_DIR / q.slug
                disk_path_old = DOCS_DIR / "quests" / q.slug
                target_dir = disk_path if disk_path.exists() else disk_path_old
                
                if target_dir.exists():
                    obj_file = target_dir / "objectives.json"
                    config_file = target_dir / "config.json"
                    if obj_file.exists():
                        try:
                            disk_data = json.loads(obj_file.read_text(encoding="utf-8"))
                            # Apply same fix
                            disk_needs_update = False
                            for o in disk_data:
                                if "rules" in o:
                                    for r in o["rules"]:
                                        if "regex" in r and "pattern" not in r:
                                            r["pattern"] = r.pop("regex")
                                            disk_needs_update = True
                            if disk_needs_update:
                                obj_file.write_text(json.dumps(disk_data, indent=2), encoding="utf-8")
                        except: pass
                
                fixed_count += 1
                print(f"  Fixed {q.slug}")
                
        if fixed_count > 0:
            await session.commit()
            print(f"✅ Fixed {fixed_count} quests.")
        else:
            print("✅ No quests needed fixing.")

if __name__ == "__main__":
    asyncio.run(fix_legacy_regex_objectives())
