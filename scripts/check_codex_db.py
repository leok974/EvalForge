import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from arcade_app.database import engine
from arcade_app.models import KnowledgeChunk

async def check_codex():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(KnowledgeChunk).where(
            KnowledgeChunk.source_id == "boss-foundry-systems-architect",
            KnowledgeChunk.source_type == "boss_codex"
        )
        result = await session.execute(stmt)
        chunk = result.scalar_one_or_none()
        
        if chunk:
            print(f"✅ Codex Chunk FOUND: {chunk.source_id}")
            print(f"   Metadata: {chunk.metadata_json}")
        else:
            print(f"❌ Codex Chunk NOT FOUND in DB.")

if __name__ == "__main__":
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(check_codex())
