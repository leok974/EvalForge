# arcade_app/seed_bosses_core.py
"""
Minimal boss seeder for Boss QA system.
Seeds world bosses (Reactor Core, Signal Prism) and ApplyLens bosses.
"""
from typing import Iterable
from sqlalchemy.orm import Session

from arcade_app.models import BossDefinition


CORE_BOSSES = [
    {
        "id": "reactor-core",
        "world_id": "world-python",
        "name": "Reactor Core",
        "description": "Master Python fundamentals: loops, state management, and defensive coding.",
        "rubric": "boss-reactor-core",
        "max_hp": 100,
    },
    {
        "id": "signal-prism",
        "world_id": "world-js",
        "name": "Signal Prism", 
        "description": "Master JavaScript/TypeScript: reducers, immutability, and event handling.",
        "rubric": "boss-signal-prism",
        "max_hp": 100,
    },
    {
        "id": "applylens-runtime-boss",
        "world_id": "project-applylens",
        "name": "Inbox Maelstrom",
        "description": "Harden ApplyLens runtime against production storm conditions.",
        "rubric": "applylens-runtime",
        "max_hp": 100,
    },
    {
        "id": "applylens-agent-boss",
        "world_id": "project-applylens",
        "name": "Intent Oracle",
        "description": "Build a safe, eval-driven agent for email triage with guardrails.",
        "rubric": "applylens-agent",
        "max_hp": 100,
    },
]


def _upsert_bosses(db: Session, bosses: Iterable[dict]) -> None:
    """Idempotently add or update boss definitions."""
    for data in bosses:
        boss_id = data["id"]

        existing = (
            db.query(BossDefinition)
            .filter(BossDefinition.id == boss_id)
            .first()
        )
        if existing:
            # Update rubric if it changed
            existing.rubric = data["rubric"]
            continue

        boss = BossDefinition(**data)
        db.add(boss)

    db.commit()


def seed_core_bosses(db: Session) -> None:
    """
    Idempotent seed for world + ApplyLens bosses needed by Boss QA.
    Safe to call on every dev/test startup.
    """
    print("🌱 Seeding core bosses for Boss QA...")
    _upsert_bosses(db, CORE_BOSSES)
    print("✅ Core bosses seeded.")


if __name__ == "__main__":
    # Standalone test
    from arcade_app.database import engine
    from sqlmodel import Session
    
    with Session(engine) as session:
        seed_core_bosses(session)
