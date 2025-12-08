import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import KnowledgeChunk, BossDefinition

async def verify_boss():
    print("Verifying Archives Query Warden integration...")
    found_boss = False
    found_codex = False
    
    async for session in get_session():
        # 1. Check Boss Definition
        stmt = select(BossDefinition).where(BossDefinition.id == "boss-archives-retrieval-query-warden")
        boss = (await session.execute(stmt)).scalar_one_or_none()
        
        if boss:
            print(f"✅ Boss Found: {boss.name}")
            print(f"   - ID: {boss.id}")
            print(f"   - World: {boss.world_id}")
            print(f"   - Rubric: {boss.rubric}")
            print(f"   - Hint Codex: {boss.hint_codex_id}")
            found_boss = True
        else:
            print("❌ Boss NOT Found!")

        # 2. Check Codex Ingestion
        codex_id = "codex.world-sql.archives-retrieval-circuit.query-warden"
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.source_id == codex_id)
        chunks = (await session.execute(stmt)).scalars().all()
        
        if chunks and len(chunks) > 0:
            print(f"✅ Codex Found: {len(chunks)} chunks")
            print(f"   - Snippet: {chunks[0].content[:50]}...")
            found_codex = True
        else:
            print(f"❌ Codex NOT Found for ID: {codex_id}")

        break # Only run once
        
    if found_boss and found_codex:
        print("\n✅ VERIFICATION SUCCESSFUL")
    else:
        print("\n❌ VERIFICATION FAILED")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_boss())
