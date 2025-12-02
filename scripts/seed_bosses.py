import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import BossDefinition

BOSS_DATA = [
    {
        "id": "reactor-core",
        "name": "The Reactor Core",
        "description": "A critical system instability. Stabilization requires precise async management.",
        "max_hp": 3,
        "time_limit_seconds": 1800, # 30 mins
        "base_xp_reward": 1000,
        "hint_codex_id": "boss-reactor-core"
    }
]

async def seed():
    print("💀 Summoning Bosses...")
    
    # Ensure tables exist
    await init_db()

    # Use the async context manager for the session
    async for session in get_session():
        count = 0
        for data in BOSS_DATA:
            # Check if exists to avoid overwrite/integrity errors
            boss = await session.get(BossDefinition, data["id"])
            if not boss:
                boss = BossDefinition(**data)
                session.add(boss)
                print(f"   + Created Boss: {data['name']}")
                count += 1
            else:
                # Update existing if needed
                for k, v in data.items():
                    setattr(boss, k, v)
                session.add(boss)
                print(f"   * Updated Boss: {data['name']}")
                
        await session.commit()
        print("✅ Bosses synced to the grid.")

if __name__ == "__main__":
    # Windows-specific event loop policy fix
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(seed())
