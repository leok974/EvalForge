import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import AvatarDefinition, AvatarVisualType, AvatarRarity

AVATARS = [
    {
        "id": "default_user",
        "name": "Initiate",
        "description": "Standard issue profile.",
        "required_level": 1,
        "rarity": "common",
        "visual_type": "icon",
        "visual_data": "user"
    },
    {
        "id": "coder_green",
        "name": "Script Kiddie",
        "description": "You wrote your first loop.",
        "required_level": 2,
        "rarity": "common",
        "visual_type": "icon",
        "visual_data": "terminal"
    },
    {
        "id": "python_gold",
        "name": "Snake Eye",
        "description": "Master of indentation.",
        "required_level": 5,
        "rarity": "rare",
        "visual_type": "icon",
        "visual_data": "code"
    },
    {
        "id": "neon_ghost",
        "name": "Netrunner",
        "description": "Ghost in the shell.",
        "required_level": 10,
        "rarity": "epic",
        "visual_type": "css",
        "visual_data": "neon-pulse"
    },
    {
        "id": "glitch_king",
        "name": "Root User",
        "description": "System access granted.",
        "required_level": 20,
        "rarity": "legendary",
        "visual_type": "css",
        "visual_data": "glitch"
    }
]

async def seed():
    print("🎨 Seeding Avatars...")
    await init_db()
    async for session in get_session():
        for data in AVATARS:
            av = AvatarDefinition(**data)
            await session.merge(av)
        await session.commit()
    print("✅ Avatars Ready.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
