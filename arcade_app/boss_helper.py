from datetime import datetime, timedelta
from sqlmodel import select
from arcade_app.models import BossDefinition, BossRun, Profile
from arcade_app.database import get_session

DEFAULT_BOSS_DURATION = 20 * 60  # 20 min

async def create_encounter(user_id: str, boss_id: str):
    async for session in get_session():
        boss = await session.get(BossDefinition, boss_id)
        if not boss:
            raise ValueError("Unknown boss_id")

        # Only one active boss per user
        stmt = select(BossRun).where(
            BossRun.user_id == user_id,
            BossRun.result == None, # Active runs have no result yet
        )
        result = await session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            return existing

        now = datetime.utcnow()
        encounter = BossRun(
            user_id=user_id,
            boss_id=boss.id,
            started_at=now,
            hp_remaining=boss.max_hp,
            # Note: BossRun doesn't have status/expires_at in the new model?
            # We might need to map them or update BossRun model.
            # For now let's assume BossRun is what we want.
        )
        session.add(encounter)
        await session.commit()
        await session.refresh(encounter)
        await session.refresh(encounter)
        return encounter

async def get_active_encounter(user_id: str):
    async for session in get_session():
        stmt = select(BossRun).where(
            BossRun.user_id == user_id,
            BossRun.result == None,
        )
        result = await session.execute(stmt)
        return result.scalars().first()

async def resolve_boss_attempt(user_id: str, encounter_id: int, score: int):
    async for session in get_session():
        enc = await session.get(BossRun, encounter_id)
        if not enc or enc.user_id != user_id:
            raise ValueError("Unknown encounter")

        # ... logic ...
        # For now, let's just update the result
        enc.score = score
        enc.result = "win" if score >= 70 else "loss" # Simplified
        enc.completed_at = datetime.utcnow()
        
        await session.commit()
        await session.refresh(enc)
        return enc, enc.result
