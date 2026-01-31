import pytest
from sqlmodel import Session
from arcade_app.models import User, TrackDefinition, QuestDefinition, BossDefinition
from arcade_app.progress_models import QuestProgressV2, QuestAttempt
from arcade_app.services.debrief_generator import get_track_status, generate_debrief

@pytest.mark.asyncio
async def test_track_completion_logic(db_session: Session):
    # 1. Setup Data
    user = User(id="test_user", name="Tester")
    db_session.add(user)
    
    # World is static concept (JSON), no DB model
    # world = WorldDefinition(id="world_java", name="Java World", slug="java")
    # db_session.add(world)
    
    track = TrackDefinition(id="track_java_basics", name="Java Basics", world_id="world_java")
    db_session.add(track)
    
    q1 = QuestDefinition(id=1, slug="java-1", title="Q1", short_description="Desc 1", world_id="world_java", track_id="track_java_basics", order_index=1)
    q2 = QuestDefinition(id=2, slug="java-2", title="Q2", short_description="Desc 2", world_id="world_java", track_id="track_java_basics", order_index=2)
    db_session.add(q1)
    db_session.add(q2)
    
    await db_session.commit()
    
    # 2. Verify Incomplete Status
    status = await get_track_status(db_session, "test_user", "world_java", "track_java_basics")
    assert status["total_n"] == 2
    assert status["completed_n"] == 0
    assert status["is_complete"] is False
    
    # 3. Complete Q1
    p1 = QuestProgressV2(user_id="test_user", quest_id="java-1", status="completed", world_id="world_java")
    db_session.add(p1)
    await db_session.commit()
    
    status = await get_track_status(db_session, "test_user", "world_java", "track_java_basics")
    assert status["completed_n"] == 1
    assert status["is_complete"] is False
    
    # 4. Complete Q2
    p2 = QuestProgressV2(user_id="test_user", quest_id="java-2", status="completed", world_id="world_java")
    db_session.add(p2)
    await db_session.commit()
    
    status = await get_track_status(db_session, "test_user", "world_java", "track_java_basics")
    assert status["completed_n"] == 2
    assert status["is_complete"] is True
    
    # 5. Verify Debrief Payload (Triggered on Q2 completion)
    # Mock attempt
    attempt = QuestAttempt(
        id="att1", 
        user_id="test_user", 
        quest_id="java-2", 
        passed=True, 
        objective_results=[{"id": "obj1", "ok": True}]
    )
    
    debrief = await generate_debrief(db_session, q2, attempt, p2)
    
    assert debrief["track_complete"] is not None
    assert debrief["track_complete"]["message"] == "Track Complete!"
    assert debrief["track_complete"]["total_n"] == 2
    
@pytest.mark.asyncio
async def test_unlock_boss_logic(db_session: Session):
    # Setup Track with Boss
    user = User(id="boss_user", name="BossTester")
    db_session.add(user)
    
    track = TrackDefinition(id="track_boss", name="Boss Track", world_id="world_java", boss_quest_id="boss_q")
    db_session.add(track)
    
    q1 = QuestDefinition(id=10, slug="boss-pre-1", title="Boss Prep", short_description="Boss Desc", world_id="world_java", track_id="track_boss", order_index=1)
    db_session.add(q1)
    
    # Boss Quest (exists but locked until track complete logic handled by frontend/backend)
    # Note: Boss unlocking is usually computed in get_track_status or debrief.
    # In generate_debrief, we check boss_quest_id
    
    await db_session.commit()
    
    # Complete Q1
    p1 = QuestProgressV2(user_id="boss_user", quest_id="boss-pre-1", status="completed", world_id="world_java")
    db_session.add(p1)
    await db_session.commit()
    
    # Check Debrief
    attempt = QuestAttempt(id="att_b", user_id="boss_user", quest_id="boss-pre-1", passed=True, objective_results=[])
    
    debrief = await generate_debrief(db_session, q1, attempt, p1)
    
    assert debrief["track_complete"] is not None
    assert debrief["track_complete"]["boss_available"] is True
    assert debrief["track_complete"]["boss_quest_id"] == "boss_q"
