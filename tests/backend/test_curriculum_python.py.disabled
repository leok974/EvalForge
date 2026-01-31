import sys
import os
import pytest
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from arcade_app.database import get_session
from arcade_app.models import QuestDefinition, UserQuest
from arcade_app.quest_helper import stream_quest_generator

# Mock track for Python Fundamentals
PYTHON_TRACK = {
    "id": "python-fundamentals",
    "name": "Python Fundamentals",
    "source": "fundamentals",
    "world_id": "world-python"
}

@pytest.mark.asyncio
async def test_python_curriculum_sequence():
    # Setup: Create a unique test user
    test_user_id = "test_user_curriculum_py"
    
    async for session in get_session():
        # Clean up all existing progress and reset sequence
        await session.execute(text("TRUNCATE TABLE userquest RESTART IDENTITY CASCADE"))
        
        # Ensure test user exists
        from arcade_app.models import User
        user = await session.get(User, test_user_id)
        if not user:
            session.add(User(id=test_user_id, name="Test User"))
            
        await session.commit()
        
        # Debug: Check UserQuest count
        count = (await session.execute(text("SELECT COUNT(*) FROM userquest"))).scalar()
        print(f"DEBUG: UserQuest count before start: {count}")
        
        # 1. First Quest: Ignition (py_01)
        # We simulate calling the generator. It should yield the quest text.
        # But we can also check the DB side effect: a new UserQuest should be created.
        
        # Trigger generator (we only need to start it to trigger the DB logic)
        gen = stream_quest_generator("start", PYTHON_TRACK, user_id=test_user_id)
        async for _ in gen: pass
        
        # Verify py_01 is active
        uq = (await session.execute(
            text(f"SELECT quest_def_id, status FROM userquest WHERE user_id = '{test_user_id}' AND status = 'active'")
        )).first()
        assert uq is not None
        assert uq.quest_def_id == "py_01"
        
        # Complete py_01
        await session.execute(text(f"UPDATE userquest SET status = 'completed' WHERE user_id = '{test_user_id}' AND quest_def_id = 'py_01'"))
        await session.commit()
        
        # 2. Second Quest: The Loop (py_02)
        gen = stream_quest_generator("next", PYTHON_TRACK, user_id=test_user_id)
        async for _ in gen: pass
        
        uq = (await session.execute(
            text(f"SELECT quest_def_id, status FROM userquest WHERE user_id = '{test_user_id}' AND status = 'active'")
        )).first()
        assert uq.quest_def_id == "py_02"
        
        # Complete py_02
        await session.execute(text(f"UPDATE userquest SET status = 'completed' WHERE user_id = '{test_user_id}' AND quest_def_id = 'py_02'"))
        await session.commit()

        # 3. Third Quest: Data Forge (py_03)
        gen = stream_quest_generator("next", PYTHON_TRACK, user_id=test_user_id)
        async for _ in gen: pass
        
        uq = (await session.execute(
            text(f"SELECT quest_def_id, status FROM userquest WHERE user_id = '{test_user_id}' AND status = 'active'")
        )).first()
        assert uq.quest_def_id == "py_03"
        
        # Complete py_03
        await session.execute(text(f"UPDATE userquest SET status = 'completed' WHERE user_id = '{test_user_id}' AND quest_def_id = 'py_03'"))
        await session.commit()
        
        # 4. Boss Quest: The Automaton (py_boss)
        gen = stream_quest_generator("next", PYTHON_TRACK, user_id=test_user_id)
        async for _ in gen: pass
        
        uq = (await session.execute(
            text(f"SELECT quest_def_id, status FROM userquest WHERE user_id = '{test_user_id}' AND status = 'active'")
        )).first()
        assert uq.quest_def_id == "py_boss"
        
        # Complete py_boss
        await session.execute(text(f"UPDATE userquest SET status = 'completed' WHERE user_id = '{test_user_id}' AND quest_def_id = 'py_boss'"))
        await session.commit()
        
        # 5. Track Complete
        gen = stream_quest_generator("next", PYTHON_TRACK, user_id=test_user_id)
        messages = []
        async for msg in gen: messages.append(msg)
        full_msg = "".join(messages)
        
        assert "TRACK COMPLETE" in full_msg

if __name__ == "__main__":
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_python_curriculum_sequence())
        print("✅ test_python_curriculum_sequence passed")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
