import os
import pytest
from sqlmodel import Session, create_engine, select
from arcade_app.models import QuestDefinition, BossDefinition, TrackDefinition

# Use sync driver for tests
DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://evalforge:evalforge@localhost:5432/evalforge", # Default to dev DB for now or use env
)

@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def session(engine):
    with Session(engine) as s:
        yield s

def test_every_core_world_has_content(session):
    # Definition of what we expect to be populated
    REQUIRED_WORLDS = {
        "world-python",
        "world-js",
        "world-sql",
        "world-infra",
        # "world-agents", # Can be agents or oracle
        "world-git", 
        "world-ml"
    }
    
    # We allow some aliasing, e.g. world-agents vs world-oracle. 
    # We check if specific tech domains are covered.
    
    quests = session.exec(select(QuestDefinition)).all()
    bosses = session.exec(select(BossDefinition)).all()
    
    # Map found worlds
    found_worlds = set()
    for q in quests:
        found_worlds.add(q.world_id)
    for b in bosses:
        if b.world_id:
            found_worlds.add(b.world_id)
            
    # Normalize aliases if needed, but for now let's just assert the sets overlap efficiently
    # actually, strictly checking the required keys is safer.
    
    missing = []
    for w in REQUIRED_WORLDS:
        if w not in found_worlds:
            # Special check for aliases
            if w == "world-agents" and "world-oracle" in found_worlds:
                continue
            missing.append(w)
            
    assert not missing, f"The following worlds are empty (no quests/bosses): {missing}"

def test_bosses_exist(session):
    bosses = session.exec(select(BossDefinition)).all()
    assert len(bosses) > 0, "No bosses found in the database!"

def test_quests_exist(session):
    quests = session.exec(select(QuestDefinition)).all()
    assert len(quests) > 0, "No quests found in the database!"
