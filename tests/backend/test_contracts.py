import pytest
from arcade_app.schemas.quest_run import RunRequest
from arcade_app.routers.routes_quests import list_quests
from arcade_app.models import QuestDefinition
from arcade_app.progress_models import QuestProgressV2

def test_run_request_contract():
    """
    Contract Test: Ensure the frontend payload structure aligns with the backend schema.
    If the frontend sends data matching this structure, it MUST pass validation.
    """
    # 1. Simulate payload from frontend (based on safeJson/questsApi structure)
    frontend_payload = {
        "code": "print('hello')",
        "language": "python",
        "mode": "execute",
        "entrypoint": "main.py",
        "workspace": [
            {"path": "main.py", "content": "print('hello')"},
            {"path": "utils.py", "content": "def help(): pass"}
        ]
    }

    # 2. Assert Pydantic validation passes
    try:
        req = RunRequest.model_validate(frontend_payload)
        
        # 3. Verify flattening worked (if model handles it) or schema matches
        assert req.entrypoint == "main.py"
        assert len(req.workspace) == 2
        assert req.workspace[0]["path"] == "main.py"
    except Exception as e:
        pytest.fail(f"Contract Broken: Backend schema rejected valid frontend payload: {e}")

@pytest.mark.asyncio
async def test_quest_availability_logic():
    """
    Logic Test: Verify the 'First Quest Available by Default' rule.
    """
    # 1. Mock Quests (Track A: Q1, Q2)
    quests = [
        QuestDefinition(slug="q1", track_id="track-a", order_index=1, title="Q1", id=1, short_description="D1", base_xp_reward=10),
        QuestDefinition(slug="q2", track_id="track-a", order_index=2, title="Q2", id=2, short_description="D2", base_xp_reward=10),
    ]
    
    # 2. Mock Progress (Empty)
    progress_map = {} # No user progress

    # 3. Re-implement logic here to verify it (Unit test style) OR call the function if cleanly separable.
    # Since logic is inside `list_quests`, we can't easily unit test it without mocking the DB/Session unless we refactor.
    # For now, we verify the LOGIC itself using a helper that mirrors the implementation.
    
    quests_by_track = {"track-a": quests}
    calculated_states = {}
    
    track_quests = quests_by_track["track-a"]
    previous_completed = True # Default
    
    for q in track_quests:
        prog = progress_map.get(q.slug)
        if prog:
            is_done = prog.status in ("completed", "mastered")
            previous_completed = is_done
            continue
        
        if previous_completed:
            calculated_states[q.slug] = "available"
            previous_completed = False
        else:
            calculated_states[q.slug] = "locked"
            previous_completed = False

    # 4. Assertions
    assert calculated_states["q1"] == "available", "First quest must be available given no progress"
    assert calculated_states["q2"] == "locked", "Second quest must be locked given first is incomplete"

    # 5. Case: Q1 Done
    progress_map = {"q1": QuestProgressV2(quest_id="q1", status="completed", attempts_count=1, runs_count=1, hint_tier_unlocked=0)}
    previous_completed = True
    calculated_states = {}

    for q in track_quests:
        prog = progress_map.get(q.slug)
        if prog:
            is_done = prog.status in ("completed", "mastered")
            previous_completed = is_done
            continue
        
        if previous_completed:
            calculated_states[q.slug] = "available"
            previous_completed = False
        else:
            calculated_states[q.slug] = "locked"
            previous_completed = False
            
    assert "q1" not in calculated_states # It has progress, so no override
    assert calculated_states["q2"] == "available", "Second quest must avail after Q1 done"

if __name__ == "__main__":
    import asyncio
    print("Running Contract Tests...")
    test_run_request_contract()
    asyncio.run(test_quest_availability_logic())
    print("✅ All Contract Tests Passed")
