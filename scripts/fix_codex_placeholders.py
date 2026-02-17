import asyncio
import os
import sys
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import models
sys.path.append(os.getcwd())
try:
    from arcade_app.models import QuestDefinition
except ImportError:
    print("Error: Could not import QuestDefinition. Run from project root.")
    sys.exit(1)

# Use correct dev credentials/port
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@127.0.0.1:5435/evalforge")

PLACEHOLDERS = ["term-1", "term-2", "term-3", "Example pending", "TODO:"]

def is_placeholder(text: str) -> bool:
    if not text:
        return False
    for p in PLACEHOLDERS:
        if p.lower() in text.lower():
            return True
    return False

async def fix_db():
    print(f"Connecting to {DATABASE_URL}...")
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with async_session() as session:
            stmt = select(QuestDefinition)
            result = await session.execute(stmt)
            quests = result.scalars().all()

            print(f"Scanning {len(quests)} quests for bad codex_references...")
            fixed_count = 0

            for q in quests:
                if not q.codex_references:
                    continue
                
                original_len = len(q.codex_references)
                # Filter out placeholders
                new_refs = [ref for ref in q.codex_references if not is_placeholder(ref)]
                
                if len(new_refs) < original_len:
                    print(f"[{q.slug}] Fixing codex_references: {q.codex_references} -> {new_refs}")
                    q.codex_references = new_refs
                    session.add(q)
                    fixed_count += 1

            if fixed_count > 0:
                print(f"\nCommitting fixes for {fixed_count} quests...")
                await session.commit()
                print("✅ Fixes applied!")
            else:
                print("\n✅ No fixes needed.")

    except Exception as e:
        print(f"Error during fix: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(fix_db())
