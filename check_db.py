import asyncio
from sqlmodel import select, func
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

async def main():
    async for session in get_session():
        # Group by world_id AND track_id
        stmt = select(QuestDefinition.world_id, QuestDefinition.track_id, func.count(QuestDefinition.id)).group_by(QuestDefinition.world_id, QuestDefinition.track_id).order_by(QuestDefinition.world_id)
        results = await session.exec(stmt)
        print(f"{'WORLD':<20} | {'TRACK':<30} | {'COUNT':<5}")
        print("-" * 60)
        for w_id, t_id, count in results.all():
            print(f"{str(w_id):<20} | {str(t_id):<30} | {count:<5}")

if __name__ == "__main__":
    asyncio.run(main())
