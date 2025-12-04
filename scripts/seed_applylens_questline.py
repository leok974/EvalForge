#!/usr/bin/env python
"""
One-off script to seed ApplyLens questline without calling the LLM.
Uses the golden spec directly.

Usage:
    python scripts/seed_applylens_questline.py
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from arcade_app.database import engine
from arcade_app.project_questline_apply import apply_project_questline_spec
from arcade_app.project_questline_spec import ProjectQuestlineSpec
from arcade_app.questmaster import APPLYLENS_QUESTLINE_GOLDEN


def main():
    if not APPLYLENS_QUESTLINE_GOLDEN:
        raise SystemExit("APPLYLENS_QUESTLINE_GOLDEN is empty")

    print("🎮 Seeding ApplyLens questline...")
    spec = ProjectQuestlineSpec.model_validate(APPLYLENS_QUESTLINE_GOLDEN)
    
    print(f"  - Project: {spec.project_name}")
    print(f"  - Template: {spec.template}")
    print(f"  - Tracks: {len(spec.tracks)}")
    print(f"  - Quests: {sum(len(t.quests) for t in spec.tracks)}")
    print(f"  - Bosses: {len(spec.bosses)}")
    
    # Apply to database
    import asyncio
    from arcade_app.database import init_db
    
    async def apply():
        # Initialize database first
        await init_db()
        
        async with engine.begin() as conn:
            def run_apply(sync_conn):
                from sqlmodel import Session
                session = Session(bind=sync_conn)
                apply_project_questline_spec(session, spec)
            
            await conn.run_sync(run_apply)
    
    asyncio.run(apply())
    print("✅ ApplyLens questline seeded successfully!")
    print("\nNext steps:")
    print("  1. Restart the backend server")
    print("  2. Navigate to QuestBoard (world: world-projects)")
    print("  3. You should see 3 tracks for ApplyLens")


if __name__ == "__main__":
    main()
