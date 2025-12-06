import asyncio
import os
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Import data and existing seeders
from arcade_app.models import QuestDefinition
from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES
from arcade_app.seed_curriculum import seed_oracle_curriculum
from arcade_app.seed_bosses import seed_bosses

# Use async driver
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge",
)

async def seed_standard_quests_async(session: AsyncSession):
    print("🌍 Seeding standard world quests (Async)...")
    for cfg in STANDARD_QUESTLINES:
        slug = cfg["slug"]
        stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
        existing = (await session.exec(stmt)).one_or_none()
        
        if existing:
            # Update fields
            existing.world_id = cfg["world_id"]
            existing.track_id = cfg["track_id"]
            existing.order_index = cfg["order_index"]
            existing.title = cfg["title"]
            existing.short_description = cfg["short_description"]
            existing.detailed_description = cfg["detailed_description"]
            existing.rubric_id = cfg["rubric_id"]
            existing.starting_code_path = cfg["starting_code_path"]
            existing.unlocks_boss_id = cfg["unlocks_boss_id"]
            existing.unlocks_layout_id = cfg["unlocks_layout_id"]
            existing.base_xp_reward = cfg["base_xp_reward"]
            existing.mastery_xp_bonus = cfg["mastery_xp_bonus"]
            session.add(existing)
        else:
            q = QuestDefinition(
                slug=slug,
                world_id=cfg["world_id"],
                track_id=cfg["track_id"],
                order_index=cfg["order_index"],
                title=cfg["title"],
                short_description=cfg["short_description"],
                detailed_description=cfg["detailed_description"],
                rubric_id=cfg["rubric_id"],
                starting_code_path=cfg["starting_code_path"],
                unlocks_boss_id=cfg["unlocks_boss_id"],
                unlocks_layout_id=cfg["unlocks_layout_id"],
                base_xp_reward=cfg["base_xp_reward"],
                mastery_xp_bonus=cfg["mastery_xp_bonus"],
            )
            session.add(q)
    
    await session.commit()
    print("✅ Standard quests seeded.")

async def main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)

    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Use a session factory needed for some functions if they don't accept passed session
    # But here we will pass session where we can, or let them use their internal mechanisms if they invoke their own engines.
    
    # NOTE: seed_oracle_curriculum and seed_bosses create their own sessions internally using 'arcade_app.database.engine' usually.
    # However, since they import 'engine' from 'arcade_app.database', and that engine instance depends on env var, 
    # we should be fine as long as DATABASE_URL env var is set correctly for them too.
    
    # 1. Standard Quests (Custom async impl using imports)
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        await seed_standard_quests_async(session)

    # 2. Oracle Curriculum (Self-contained)
    await seed_oracle_curriculum()

    # 3. Bosses (Self-contained)
    await seed_bosses()

    await engine.dispose()
    print("✅ EvalForge universe seeded successfully.")

if __name__ == "__main__":
    asyncio.run(main())
