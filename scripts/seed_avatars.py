import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import AvatarDefinition

AVATARS = [
    {
        "id": "default_user",
        "name": "Initiate",
        "description": "Baseline identity. No augmentations installed.",
        "required_level": 1,
        "rarity": "common",
        "visual_type": "icon",
        "visual_data": "user",  # lucide icon key
    },
    {
        "id": "coder_green",
        "name": "Script Kiddie",
        "description": "Emerald terminal glow.",
        "required_level": 2,
        "rarity": "common",
        "visual_type": "icon",
        "visual_data": "terminal",
    },
    {
        "id": "python_gold",
        "name": "Snake Eye",
        "description": "Golden code sigil.",
        "required_level": 5,
        "rarity": "rare",
        "visual_type": "icon",
        "visual_data": "code",
    },
    {
        "id": "neon_ghost",
        "name": "Netrunner",
        "description": "Glowing cyan silhouette. Pulses with traffic.",
        "required_level": 10,
        "rarity": "epic",
        "visual_type": "css",
        "visual_data": "neon-pulse",
    },
    {
        "id": "glitch_king",
        "name": "Root User",
        "description": "Red/black avatar that glitches reality.",
        "required_level": 20,
        "rarity": "epic",
        "visual_type": "css",
        "visual_data": "glitch",
    },
    {
        "id": "void_walker",
        "name": "Architect",
        "description": "Animated starfield masked into a circle.",
        "required_level": 50,
        "rarity": "legendary",
        "visual_type": "css",
        "visual_data": "cosmic",
    },
]


async def seed():
    print("🎭 Seeding Avatar Definitions...")
    await init_db()
    async for session in get_session():
        for data in AVATARS:
            avatar = AvatarDefinition(**data)
            # upsert via merge
            await session.merge(avatar)
        await session.commit()
    print(f"✅ Loaded {len(AVATARS)} avatars.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
