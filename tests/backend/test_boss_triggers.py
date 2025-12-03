import pytest
from arcade_app.boss_triggers import BossTriggerContext, maybe_trigger_boss
from arcade_app.models import Profile, BossDefinition, UserQuest, QuestDefinition
from sqlmodel import Session

@pytest.fixture
def boss_definition(db_session: Session):
    boss = BossDefinition(
        id="boss-test",
        name="Test Boss",
        world_id="world-test",
        track_id="track-test",
        enabled=True
    )
    db_session.add(boss)
    db_session.commit()
    return boss

@pytest.fixture
def profile(db_session: Session):
    from arcade_app.models import User
    user = User(id="test-user", name="Test User")
    db_session.add(user)
    db_session.commit()
    
    profile = Profile(user_id="test-user")
    db_session.add(profile)
    db_session.commit()
    return profile

@pytest.mark.asyncio
async def test_no_boss_before_minimum_quests(db_session, profile, boss_definition):
    ctx = BossTriggerContext(
        profile=profile,
        world_id=boss_definition.world_id,
        track_id=boss_definition.track_id,
        quest_id="q1",
        was_boss=False,
        passed=True,
        grade="A",
        attempts_on_track=3,
        completed_quests_on_track=1,  # below min=3
    )

    boss = await maybe_trigger_boss(ctx, session=db_session)
    assert boss is None


@pytest.mark.asyncio
async def test_boss_triggers_after_threshold(monkeypatch, db_session, profile, boss_definition):
    # force RNG
    monkeypatch.setattr("arcade_app.boss_triggers.random.random", lambda: 0.01)

    ctx = BossTriggerContext(
        profile=profile,
        world_id=boss_definition.world_id,
        track_id=boss_definition.track_id,
        quest_id="q3",
        was_boss=False,
        passed=True,
        grade="A",
        attempts_on_track=3,
        completed_quests_on_track=5,
    )

    boss = await maybe_trigger_boss(ctx, session=db_session)
    assert boss is not None
    assert boss.id == boss_definition.id
