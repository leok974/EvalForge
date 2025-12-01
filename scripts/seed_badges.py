import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import BadgeDefinition

BADGES = [
    # --- GENERAL & ONBOARDING ---
    {
        "id": "hello_world",
        "name": "Hello World",
        "description": "Complete your first Quest.",
        "icon": "👋",
        "rarity": "common",
        "xp_bonus": 50,
        "category": "general"
    },
    {
        "id": "repo_hoarder",
        "name": "Librarian",
        "description": "Sync 3 different repositories.",
        "icon": "📚",
        "rarity": "rare",
        "xp_bonus": 300,
        "category": "collection"
    },
    {
        "id": "perfectionist",
        "name": "10x Engineer",
        "description": "Achieve a 100% score on a Judge Evaluation.",
        "icon": "✨",
        "rarity": "epic",
        "xp_bonus": 500,
        "category": "skill"
    },

    # --- LEVELING MILESTONES ---
    {
        "id": "level_5",
        "name": "Junior Dev",
        "description": "Reach Global Level 5.",
        "icon": "🌱",
        "rarity": "common",
        "xp_bonus": 200,
        "category": "progression"
    },
    {
        "id": "level_10",
        "name": "Mid-Level",
        "description": "Reach Global Level 10.",
        "icon": "🛠️",
        "rarity": "rare",
        "xp_bonus": 1000,
        "category": "progression"
    },
    {
        "id": "level_50",
        "name": "Staff Engineer",
        "description": "Reach Global Level 50.",
        "icon": "🧙‍♂️",
        "rarity": "legendary",
        "xp_bonus": 5000,
        "category": "progression"
    },

    # --- PYTHON WORLD ---
    {
        "id": "python_novice",
        "name": "Snake Charmer",
        "description": "Complete 5 Quests in Python World.",
        "icon": "🐍",
        "rarity": "common",
        "xp_bonus": 150,
        "category": "world-python"
    },
    {
        "id": "python_master",
        "name": "Pythonista",
        "description": "Complete the Python World (20 Quests).",
        "icon": "👑",
        "rarity": "epic",
        "xp_bonus": 1000,
        "category": "world-python"
    },
    {
        "id": "boss_python",
        "name": "GIL Slayer",
        "description": "Defeat the Python World Boss (Pass a Hard Evaluation).",
        "icon": "⚔️",
        "rarity": "legendary",
        "xp_bonus": 2000,
        "category": "combat"
    },

    # --- INFRA WORLD ---
    {
        "id": "infra_architect",
        "name": "Cloud Atlas",
        "description": "Complete 5 Quests in Infra World.",
        "icon": "☁️",
        "rarity": "rare",
        "xp_bonus": 300,
        "category": "world-infra"
    },
    {
        "id": "boss_infra",
        "name": "Downtime Destroyer",
        "description": "Defeat the Infra World Boss (Fix a System Outage).",
        "icon": "🛡️",
        "rarity": "legendary",
        "xp_bonus": 2000,
        "category": "combat"
    },

    # --- AGENT WORLD ---
    {
        "id": "agent_whisperer",
        "name": "Prompt Engineer",
        "description": "Complete 5 Quests in Agents World.",
        "icon": "🤖",
        "rarity": "rare",
        "xp_bonus": 300,
        "category": "world-agents"
    },
]

async def seed_badges():
    print("🏆 Seeding Badge Definitions...")
    
    # Ensure DB exists
    await init_db()

    async for session in get_session():
        count = 0
        for badge_data in BADGES:
            badge = BadgeDefinition(**badge_data)
            # Upsert (Merge) logic
            await session.merge(badge)
            count += 1
        
        await session.commit()
        print(f"✅ Loaded {count} badges into the catalog.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_badges())
