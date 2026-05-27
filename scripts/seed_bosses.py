import asyncio
import json
import sys
import os
from pathlib import Path

# Add root to path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

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


def _load_boss_objectives(questpack_path: str, boss_slug: str) -> list:
    """
    Load the objectives array from the boss quest entry in a questpack file.

    The boss quest is identified by matching slug == boss_slug.  Returns [] if
    the pack or quest cannot be found, so callers can always destructure safely.
    """
    p = ROOT / questpack_path
    if not p.exists():
        print(f"   [WARN] questpack not found: {questpack_path}")
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"   [WARN] could not parse {questpack_path}: {e}")
        return []

    raw: list = []
    if isinstance(data, list):
        raw = data
    elif isinstance(data, dict):
        raw = data.get("quests") or data.get("entries") or []

    for quest in raw:
        if isinstance(quest, dict) and quest.get("slug") == boss_slug:
            return quest.get("objectives") or []

    print(f"   [WARN] boss slug {boss_slug!r} not found in {questpack_path}")
    return []


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
    # --- World-Docker: Microservice Stack (deterministic objectives + LLM rubric) ---
    {
        "id": "boss-docker-microservice-stack",
        "name": "Docker Microservice Stack",
        "description": (
            "Design a production-ready three-tier stack: nginx reverse proxy, Python API, and Postgres "
            "database — wired with named networks, named volumes, healthchecks, and restart policies."
        ),
        "technical_objective": (
            "Submit a compose.yaml that defines api, db, and nginx services connected via a "
            "named network, uses a named volume for Postgres persistence, includes a db healthcheck, "
            "and has api depend on db."
        ),
        "world_id": "world-docker",
        "track_id": "track-docker-systems",
        "rubric": _load_rubric("rubrics/boss-docker-microservice-stack.json"),
        # Sprint 19: load deterministic objectives from the questpack so they stay in sync
        "objectives_json": _load_boss_objectives(
            "data/questpacks/docker_systems.json",
            "dk-boss-microservice-stack",
        ),
        "base_xp_reward": 1200,
        "difficulty": "hard",
        "hint_codex_id": "boss-docker-microservice-stack",
        "enabled": True,
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
