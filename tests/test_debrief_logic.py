import pytest
from unittest.mock import MagicMock
from datetime import datetime
from sqlmodel import Session
from arcade_app.services.debrief_generator import generate_debrief, recommend_next_quest
from arcade_app.models import QuestDefinition, QuestState
from arcade_app.progress_models import QuestAttempt, QuestProgressV2

@pytest.mark.asyncio
async def test_debrief_generation():
    # Mock Objects
    session = MagicMock(spec=Session)
    
    # 1. Setup Quest
    quest = QuestDefinition(
        slug="test-quest",
        title="Test Quest",
        track_id="track-alpha",
        order_index=1,
        objectives_json=[
            {"id": "obj1", "title": "Print Hello"},
            {"id": "obj2", "title": "Use Loop"}
        ],
        state=QuestState.AVAILABLE # type: ignore
    )
    
    # 2. Setup Attempt (Passed)
    attempt = QuestAttempt(
        user_id="user1",
        quest_id="test-quest",
        passed=True,
        objective_results=[
            {"id": "obj1", "ok": True},
            {"id": "obj2", "ok": True}
        ],
        test_summary_json={"passed": 2, "failed": 0}
    )
    
    # 3. Setup Progress
    prog = QuestProgressV2(
        user_id="user1",
        quest_id="test-quest",
        status="completed"
    )
    
    # Mock recommend_next_quest to avoid DB call in unit test or mock DB
    # We will test recommend_next_quest separately or integrate mock
    
    # Mocking session.exec to simulate fetching next quest for recommendation
    # But generate_debrief calls it.
    # Ideally integration test with DB is better, but unit test is faster.
    # Let's mock the `recommend_next_quest` function call? 
    # Hard to mock imported function in same module easily without patching module interactively.
    # Instead, let's just let it run and mock the DB query response.
    
    next_quest = QuestDefinition(
        slug="next-quest",
        title="Next Quest",
        track_id="track-alpha",
        order_index=2,
        state=QuestState.AVAILABLE # type: ignore
    )
    
    # Mock session.exec for recommend_next_quest
    # It calls: stmt = select(QuestDefinition).where...
    # Then session.exec(stmt).all()
    # Then select(QuestProgressV2)...
    
    class MockResult:
        def all(self):
            return [quest, next_quest]
        def first(self):
            return None # No progress on next quest
            
    session.exec.return_value = MockResult()
    
    # Auto-mocking async exec is tricky if not awaiting properly. 
    # `session.exec` in SQLModel is sync but called with `await`? No, SQLModel sync. 
    # `await session.exec` is for AsyncSession.
    # `debrief_generator` uses `await session.exec(...)`.
    # So we need an AsyncMock.
    
    async def mock_exec(*args, **kwargs):
        return MockResult()
        
    session.exec = mock_exec
    
    # Run
    debrief = await generate_debrief(session, quest, attempt, prog)
    
    assert debrief["title"] == "Mission Accomplished"
    assert "obj1" in debrief["passed_objectives"]
    assert len(debrief["objective_titles"]) == 2
    assert "You successfully completed all objectives." in debrief["learning_points"] or len(debrief["learning_points"]) > 0
    assert debrief["next"] is not None
    assert debrief["next"]["quest_id"] == "next-quest"
    print("Debrief Generated:", debrief)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_debrief_generation())
