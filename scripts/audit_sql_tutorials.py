import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def audit():
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    bucket_a = [] # Missing file on disk
    bucket_b = [] # File exists but DB is blank or pure placeholder
    golden = []   # Looks good
    
    async with Session() as s:
        r = await s.execute(select(QuestDefinition).where(QuestDefinition.world_id == 'world-sql'))
        quests = r.scalars().all()
        
        for q in quests:
            slug = q.slug
            disk_path = Path(f"docs/quests/{slug}/tutorial.md")
            
            # 1. Check disk existence
            if not disk_path.exists():
                bucket_a.append(slug)
                continue
                
            disk_content = disk_path.read_text(encoding="utf-8")
            
            # 2. Check DB sync and content quality
            db_content = q.tutorial_md or ""
            is_placeholder = "What you'll build" in db_content and "Example logic" in db_content
            
            if not db_content or is_placeholder:
                bucket_b.append(slug)
            else:
                golden.append(slug)

    print("\\n=== SQL TUTORIAL AUDIT ===")
    print(f"Total SQL Quests: {len(quests)}")
    print(f"\\n🏆 Golden / Custom: {len(golden)}")
    for s in golden:
        print(f"  - {s}")
        
    print(f"\\n🪣  Bucket A (Missing on disk): {len(bucket_a)}")
    for s in bucket_a:
        print(f"  - {s}")

    print(f"\\n🪣  Bucket B (File exists, but DB is blank/placeholder): {len(bucket_b)}")
    for s in bucket_b:
        print(f"  - {s}")
        
    print("\\nRecommended Next Target:")
    if bucket_b:
        print(f"👉 {bucket_b[0]}")
    elif bucket_a:
        print(f"👉 {bucket_a[0]}")

if __name__ == "__main__":
    asyncio.run(audit())
