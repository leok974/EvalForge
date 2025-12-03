from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from arcade_app.models import BossDefinition, KnowledgeChunk
from arcade_app.database import engine

REACTOR_STARTING_CODE = """# reactor.py
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/reactor/status")
def reactor_status():
    # Simulate slow blocking I/O
    time.sleep(3)
    return {"status": "stable", "temperature": 900}
"""

REACTOR_RUBRIC = """
Scoring (0–100):

Async correctness (0–40 pts)
- async def on the route (10)
- At least one await in the function body (10)
- No time.sleep anywhere (10)
- Uses asyncio.sleep or equivalent (10)

Model & typing (0–30 pts)
- ReactorStatus model present, subclass of BaseModel (10)
- Has fields status: str and temperature: int (10)
- Route annotated to return ReactorStatus and/or uses response_model (10)

Structure & clarity (0–20 pts)
- Helper async def fetch_reactor_status() exists (10)
- Endpoint uses helper instead of inlining everything (5)
- No obvious junk / debug prints / unused imports (5)

Style & extras (0–10 pts)
- Good naming, docstring, or small extra (e.g. handling delay as a param).
"""

async def seed_bosses():
    print("🌱 Seeding Bosses...")
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # 1. Reactor Core
        boss_id = "boss-reactor-core"
        stmt = select(BossDefinition).where(BossDefinition.id == boss_id)
        existing = (await session.execute(stmt)).scalar_one_or_none()

        if not existing:
            print(f"  - Creating {boss_id}")
            boss = BossDefinition(
                id=boss_id,
                name="The Reactor Core",
                description="A high-pressure backend service that demands async correctness and robust error handling.",
                technical_objective="Implement a stable reactor status endpoint that handles high load without blocking.",
                rubric=REACTOR_RUBRIC,
                world_id="world-python",
                track_id="backend-api",
                time_limit_seconds=1800,
                max_hp=100,
                difficulty="hard",
                hint_codex_id="boss-reactor-core-strategy", # Linked Strategy Guide
                enabled=True
            )
            session.add(boss)
        else:
            print(f"  - Updating {boss_id}")
            existing.hint_codex_id = "boss-reactor-core-strategy"
            existing.technical_objective = "Implement a stable reactor status endpoint that handles high load without blocking."
            existing.rubric = REACTOR_RUBRIC
            session.add(existing)
        
        await session.commit()

        # 2. Seed Codex Docs (Strategy Guide)
        print("  - Seeding Codex Docs...")
        codex_docs = [
            {
                "tier": 1,
                "slug": "reactor-core-tier-1",
                "title": "Reactor Core: Basic Analysis",
                "content": """# Reactor Core: Basic Analysis
The reactor core is a high-throughput system.
Key observations:
- The `reactor_status` endpoint is slow.
- It uses `time.sleep(3)`, which blocks the event loop.
- This causes the server to become unresponsive under load.
"""
            },
            {
                "tier": 2,
                "slug": "reactor-core-tier-2",
                "title": "Reactor Core: Async Patterns",
                "content": """# Reactor Core: Async Patterns
To fix the blocking issue:
1. Use `async def` for the route handler.
2. Replace `time.sleep()` with `asyncio.sleep()`.
3. Ensure the return type matches the Pydantic model.
"""
            },
            {
                "tier": 3,
                "slug": "reactor-core-tier-3",
                "title": "Reactor Core: Advanced Optimization",
                "content": """# Reactor Core: Advanced Optimization
For maximum performance:
- Offload heavy computation to a thread pool if needed.
- Use caching for status if it doesn't change often.
- Add proper error handling for sensor failures.
"""
            }
        ]

        for doc in codex_docs:
            stmt = select(KnowledgeChunk).where(KnowledgeChunk.source_id == doc["slug"])
            existing_chunk = (await session.execute(stmt)).scalar_one_or_none()
            
            if not existing_chunk:
                chunk = KnowledgeChunk(
                    source_type="codex",
                    source_id=doc["slug"],
                    chunk_index=0,
                    content=doc["content"],
                    embedding=[0.0]*768, # Dummy embedding
                    metadata_json={
                        "boss_id": "boss-reactor-core",
                        "tier": doc["tier"],
                        "title": doc["title"]
                    }
                )
                session.add(chunk)
            else:
                existing_chunk.content = doc["content"]
                existing_chunk.metadata_json = {
                    "boss_id": "boss-reactor-core",
                    "tier": doc["tier"],
                    "title": doc["title"]
                }
                session.add(existing_chunk)

        await session.commit()
    print("✅ Bosses Seeded.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_bosses())
