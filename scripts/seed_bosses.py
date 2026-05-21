import asyncio
import json
import sys
import os
from pathlib import Path

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import BossDefinition


def _load_rubric(path: str) -> str:
    """Load a rubric JSON file and return it as a compact JSON string."""
    p = Path(path)
    if not p.exists():
        return ""
    try:
        return json.dumps(json.loads(p.read_text(encoding="utf-8")))
    except Exception:
        return ""


BOSS_DATA = [
    # --- World-Python: Systems Architect (LLM-judged, rubric-based) ---
    {
        "id": "boss-foundry-systems-architect",
        "name": "Foundry Systems Architect",
        "description": (
            "Design a resilient, observable Python service. "
            "Demonstrate clean architecture, circuit breakers, structured logging, and async queues."
        ),
        "world_id": "world-python",
        "track_id": "track-python-systems",
        "rubric": _load_rubric("rubrics/boss-foundry-systems-architect.json"),
        "base_xp_reward": 1500,
        "difficulty": "hard",
        "hint_codex_id": "boss-foundry-systems-architect",
        "enabled": True,
    },
    # --- Legacy: Reactor Core (kept for backward compat) ---
    {
        "id": "reactor-core",
        "name": "The Reactor Core",
        "description": "A critical system instability. Stabilization requires precise async management.",
        "world_id": "world-python",
        "track_id": "track-python-systems",
        "base_xp_reward": 1000,
        "hint_codex_id": "boss-reactor-core",
        "enabled": False,  # Superseded by boss-foundry-systems-architect
    },
]


async def seed():
    # Force UTF-8 output for Windows terminals
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("[seed] Summoning Bosses...")

    # Ensure tables exist
    await init_db()

    # Use the async context manager for the session
    async for session in get_session():
        for data in BOSS_DATA:
            boss = await session.get(BossDefinition, data["id"])
            if not boss:
                boss = BossDefinition(**data)
                session.add(boss)
                print(f"   + Created Boss: {data['name']}")
            else:
                for k, v in data.items():
                    setattr(boss, k, v)
                session.add(boss)
                print(f"   * Updated Boss: {data['name']}")

        await session.commit()
        print("[seed] Bosses synced to the grid.")


if __name__ == "__main__":
    # Windows-specific event loop policy fix
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(seed())
