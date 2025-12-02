import sys
import os
import json
import asyncio
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from arcade_app.agent import QuestAgent, JudgeAgent, ExplainAgent, DebugAgent

@pytest.mark.asyncio
async def test_quest_agent_emits_npc_identity_first():
    agent = QuestAgent()
    context = {"track_id": "python-fundamentals", "world_id": "world-python", "objective": "Print 'hello'."}
    events = []
    async for ev in agent.run("start", context):
        events.append(ev)
        if len(events) >= 1:
            break

    assert events[0]["event"] == "npc_identity"
    npc = json.loads(events[0]["data"])
    assert npc["name"] == "KAI"

@pytest.mark.asyncio
async def test_judge_agent_emits_npc_identity():
    agent = JudgeAgent()
    context = {"track_id": "python-fundamentals", "user_id": "test"}
    events = []
    # We expect it to fail grading or something, but first event should be identity
    try:
        async for ev in agent.run("print('hello')", context):
            events.append(ev)
            if len(events) >= 1:
                break
    except Exception:
        pass # Ignore downstream errors

    assert events[0]["event"] == "npc_identity"
    npc = json.loads(events[0]["data"])
    assert npc["name"] == "ZERO"

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_quest_agent_emits_npc_identity_first())
        print("✅ test_quest_agent_emits_npc_identity_first passed")
        loop.run_until_complete(test_judge_agent_emits_npc_identity())
        print("✅ test_judge_agent_emits_npc_identity passed")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
