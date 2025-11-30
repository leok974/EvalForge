import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import KnowledgeChunk

async def check_db():
    print("Checking database contents...")
    async for session in get_session():
        result = await session.execute(select(KnowledgeChunk))
        chunks = result.scalars().all()
        print(f"\nTotal chunks in database: {len(chunks)}")
        
        if chunks:
            print("\nFirst 3 chunks:")
            for i, chunk in enumerate(chunks[:3]):
                print(f"\n{i+1}. Source: {chunk.source_id}")
                print(f"   Type: {chunk.source_type}")
                print(f"   Content preview: {chunk.content[:100]}...")
        else:
            print("No chunks found. Run 'python scripts/ingest_codex.py' first.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_db())
