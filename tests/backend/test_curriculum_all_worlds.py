import sys
import os
import pytest
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

FUNDAMENTALS_TRACKS = [
    "python-fundamentals",
    "js-fundamentals",
    "sql-fundamentals",
    "infra-fundamentals",
    "agent-fundamentals",
    "git-fundamentals",
    "ml-fundamentals",
]

@pytest.mark.asyncio
async def test_every_fundamentals_track_has_curriculum():
    async for session in get_session():
        for track_id in FUNDAMENTALS_TRACKS:
            # Fetch all quests for this track, ordered by sequence
            result = await session.execute(
                text(f"SELECT id, title, sequence_order FROM questdefinition WHERE track_id = '{track_id}' ORDER BY sequence_order ASC")
            )
            quests = result.fetchall()
            
            print(f"Checking {track_id}: Found {len(quests)} quests.")
            
            # 1. Must have quests
            assert len(quests) >= 3, f"Track {track_id} has fewer than 3 quests ({len(quests)})"
            
            # 2. Must start at sequence 1
            assert quests[0].sequence_order == 1, f"Track {track_id} does not start at sequence 1"
            
            # 3. Must have a BOSS
            boss_quests = [q for q in quests if "BOSS" in q.title.upper()]
            assert len(boss_quests) >= 1, f"Track {track_id} missing a BOSS quest"
            
            # 4. Boss should be the last one (usually)
            assert quests[-1].id == boss_quests[-1].id, f"Track {track_id} boss is not the last quest"

if __name__ == "__main__":
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_every_fundamentals_track_has_curriculum())
        print("✅ test_every_fundamentals_track_has_curriculum passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
