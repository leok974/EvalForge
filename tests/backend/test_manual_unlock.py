import pytest
from arcade_app.models import User, Profile, QuestDefinition, QuestProgress, QuestState
from arcade_app.practice.constants import STARTER_WORLD_SLUG, STARTER_QUEST_ID
from arcade_app.practice.starter import ensure_starter_unlocked
from sqlmodel import select

@pytest.mark.asyncio
async def test_manual_unlock_logic(db_session):
    session = db_session
    user_id = "manual_test_user"
    
    # 1. Setup
    user = User(id=user_id, name="Manual User")
    session.add(user)
    profile = Profile(user_id=user_id)
    session.add(profile)
    
    q_def = QuestDefinition(
        slug=STARTER_QUEST_ID,
        title="Starter",
        short_description="Start",
        world_id=STARTER_WORLD_SLUG,
        track_id="t1"
    )
    session.add(q_def)
    await session.commit()
    await session.refresh(profile)
    
    # 2. Call Function Logic
    await ensure_starter_unlocked(session, profile)
    
    # 3. Assert
    qp = (await session.exec(select(QuestProgress).where(QuestProgress.user_id == user_id))).first()
    assert qp is not None, "QuestProgress not created by ensure_starter_unlocked"
    assert qp.state == QuestState.AVAILABLE
