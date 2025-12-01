import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import SkillNode

SKILLS = [
    # --- TIER 1: THE BASICS (Cost: 1) ---
    {
        "id": "visual_optics",
        "name": "Optical Enhancer",
        "description": "Enables syntax highlighting for code blocks.",
        "cost": 1,
        "tier": 1,
        "category": "visual",
        "feature_key": "syntax_highlighting",
        "parent_id": None
    },
    {
        "id": "archive_uplink",
        "name": "Archive Uplink",
        "description": "Grant access to the Codex knowledge base.",
        "cost": 1,
        "tier": 1,
        "category": "system",
        "feature_key": "codex_access",
        "parent_id": None
    },

    # --- TIER 2: INTELLIGENCE (Cost: 2) ---
    {
        "id": "module_elara",
        "name": "Mentor Protocol",
        "description": "Unlock ELARA (Explain Agent) for conceptual help.",
        "cost": 2,
        "tier": 2,
        "category": "agent",
        "feature_key": "agent_explain",
        "parent_id": "archive_uplink"
    },
    {
        "id": "module_linter",
        "name": "Static Analyzer",
        "description": "The Judge provides line-specific syntax feedback.",
        "cost": 2,
        "tier": 2,
        "category": "analysis",
        "feature_key": "judge_linter",
        "parent_id": "visual_optics"
    },

    # --- TIER 3: DEEP TECH (Cost: 3) ---
    {
        "id": "module_patch",
        "name": "Debug Routine",
        "description": "Unlock PATCH (Debug Agent) to fix broken code.",
        "cost": 3,
        "tier": 3,
        "category": "agent",
        "feature_key": "agent_debug",
        "parent_id": "module_elara"
    },
    {
        "id": "deep_scan",
        "name": "Deep Scan",
        "description": "Allows Agents to read your Project Files (RAG).",
        "cost": 3,
        "tier": 3,
        "category": "system",
        "feature_key": "repo_rag",
        "parent_id": "archive_uplink"
    }
]

async def seed():
    print("🧬 Seeding Tech Tree...")
    await init_db()
    async for session in get_session():
        count = 0
        for data in SKILLS:
            # Upsert logic
            skill = SkillNode(**data)
            await session.merge(skill)
            count += 1
        await session.commit()
    print(f"✅ Tech Tree Online: {count} Nodes.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
