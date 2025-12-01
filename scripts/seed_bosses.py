import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from arcade_app.database import init_db, get_session
from arcade_app.models import BossDefinition
from sqlmodel import select

BOSSES = [
    {
        "id": "boss-reactor-core",
        "world_id": "world-python",
        "track_id": None,
        "title": "Reactor Core Meltdown",
        "slugline": "Contain the breach before meltdown",
        "technical_objective": "Fix the async reactor monitoring system using proper asyncio patterns and Pydantic models",
        "starting_code": """import asyncio
from pydantic import BaseModel

# TODO: Define ReactorStatus model

# TODO: Implement async reactor_status function

# TODO: Implement fetch_reactor_status wrapper
""",
        "rubric": """Evaluate based on:
1. Async Implementation (40 points): Proper use of async/await, asyncio.sleep
2. Pydantic Model (30 points): ReactorStatus model with correct fields
3. Code Structure (20 points): Clean function definitions, proper imports
4. Style (10 points): Docstrings, naming conventions
""",
        "time_limit_seconds": 30 * 60,  # 30 minutes
        "pass_threshold": 70,
        "xp_reward": 300,
        "integrity_damage": 10,
        "difficulty": "normal",
    },
    {
        "id": "boss-reactor-core-hard",
        "world_id": "world-python",
        "track_id": None,
        "title": "Reactor Core – HARD MODE",
        "slugline": "Critical systems failing fast",
        "technical_objective": "Fix the reactor system with stricter requirements and time pressure",
        "starting_code": """import asyncio
from pydantic import BaseModel

# TODO: More complex reactor challenge
""",
        "rubric": """Strict evaluation:
1. Async Implementation (40 points): Advanced patterns, error handling
2. Pydantic Model (30 points): Complex validation, custom validators
3. Code Structure (20 points): Modular design, type hints
4. Style (10 points): Complete documentation, perfect naming
""",
        "time_limit_seconds": 15 * 60,  # 15 minutes
        "pass_threshold": 80,
        "xp_reward": 600,
        "integrity_damage": 20,
        "difficulty": "hard",
    },
]

async def seed():
    await init_db()
    async for session in get_session():
        for data in BOSSES:
            # Check if boss already exists
            result = await session.exec(
                select(BossDefinition).where(BossDefinition.id == data["id"])
            )
            existing = result.one_or_none()
            
            if existing:
                # Update existing boss
                for key, value in data.items():
                    setattr(existing, key, value)
                print(f"Updated boss: {data['id']}")
            else:
                # Create new boss
                boss = BossDefinition(**data)
                session.add(boss)
                print(f"Created boss: {data['id']}")
        
        await session.commit()
        print(f"Seeded {len(BOSSES)} bosses.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
