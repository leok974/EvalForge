import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import KnowledgeChunk, BossDefinition

async def verify_boss():
    print("Verifying Grid Sandbox Warden integration...")
    found_boss = False
    found_codex = False
    found_rubric = False
    
    async for session in get_session():
        # 1. Check Boss Definition
        stmt = select(BossDefinition).where(BossDefinition.id == "boss-grid-containment-sandbox-warden")
        boss = (await session.execute(stmt)).scalar_one_or_none()
        
        if boss:
            print(f"✅ Boss Found: {boss.name}")
            print(f"   - ID: {boss.id}")
            print(f"   - World: {boss.world_id}")
            print(f"   - Rubric: {boss.rubric}")
            print(f"   - Hint Codex: {boss.hint_codex_id}")
            
            # Check if rubric points to the right ID
            if boss.rubric == "boss-grid-containment-sandbox-warden":
                print("   ✅ Rubric ID matches convention")
            else:
                print(f"   ⚠️ Rubric ID mismatch: {boss.rubric}")
                
            found_boss = True
        else:
            print("❌ Boss NOT Found!")

        # 2. Check Codex Ingestion
        codex_id = "codex.world-infra.grid-containment.sandbox-warden"
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.source_id == codex_id)
        chunks = (await session.execute(stmt)).scalars().all()
        
        if chunks and len(chunks) > 0:
            print(f"✅ Codex Found: {len(chunks)} chunks")
            found_codex = True
        else:
            print(f"❌ Codex NOT Found for ID: {codex_id}")

        # 3. Check Rubric Ingestion
        rubric_id = "boss-grid-containment-sandbox-warden"
        stmt = select(KnowledgeChunk).where(
            (KnowledgeChunk.source_id == rubric_id) & 
            (KnowledgeChunk.source_type == "boss_rubric")
        )
        chunks = (await session.execute(stmt)).scalars().all()
        
        if chunks and len(chunks) > 0:
            print(f"✅ Rubric Chunk Found: {len(chunks)} chunks")
            found_rubric = True
        else:
            print(f"❌ Rubric Chunk NOT Found for ID: {rubric_id}")

        break 
        
    if found_boss and found_codex and found_rubric:
        print("\n✅ VERIFICATION SUCCESSFUL")
    else:
        print("\n❌ VERIFICATION FAILED")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_boss())
