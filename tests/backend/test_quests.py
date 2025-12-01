import pytest
import pytest_asyncio
import sys
from unittest.mock import AsyncMock, patch, MagicMock
from sqlmodel import select
from arcade_app.models import User, QuestDefinition, UserQuest, QuestSource
from arcade_app.quest_helper import stream_quest_generator

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def curriculum_setup(db_session):
    """Seeds a mini curriculum."""
    # 1. User
    user = User(id="student", name="Student")
    db_session.add(user)
    
    # 2. Quests (Seq 1 & 2)
    q1 = QuestDefinition(
        id="q1", track_id="test-track", sequence_order=1,
        title="Lesson 1", technical_objective="Do X", rubric_hints="Check X", xp_reward=10
    )
    q2 = QuestDefinition(
        id="q2", track_id="test-track", sequence_order=2,
        title="Lesson 2", technical_objective="Do Y", rubric_hints="Check Y", xp_reward=20
    )
    db_session.add(q1)
    db_session.add(q2)
    
    await db_session.commit()

async def test_fundamentals_start(db_session, curriculum_setup):
    """Verify a new user gets Quest 1."""
    track = {"id": "test-track", "name": "Test Track", "source": "fundamentals"}
    
    # Mock Vertex AI
    mock_model = MagicMock()
    mock_model.generate_content_async = AsyncMock(return_value=AsyncMock(__aiter__=lambda self: iter([])))
    
    # Patch get_session to use our test db_session
    async def mock_get_session():
        yield db_session

    # We need to mock vertexai.generative_models.GenerativeModel
    # Since it is imported inside the function, we can patch the module if it exists, 
    # or we can mock the import using sys.modules if it doesn't.
    # Assuming it exists or we can patch the import path.
    # If the import happens inside the function, patch('vertexai.generative_models.GenerativeModel') works 
    # IF the module is importable.
    
    # Let's try to mock the module in sys.modules to be safe
    mock_vertexai = MagicMock()
    mock_vertexai.generative_models.GenerativeModel = MagicMock(return_value=mock_model)
    
    with patch.dict(sys.modules, {"vertexai": mock_vertexai, "vertexai.generative_models": mock_vertexai.generative_models}), \
         patch("arcade_app.quest_helper.get_session", side_effect=mock_get_session):
        
        # Run Generator
        async for _ in stream_quest_generator("start", track, "student"):
            pass
            
        # 1. Check DB for Active Quest
        uq = (await db_session.execute(
            select(UserQuest).where(UserQuest.user_id == "student")
        )).scalars().first()
        
        assert uq is not None
        assert uq.quest_def_id == "q1"
        assert uq.status == "active"
        
        # 2. Check Prompt Content
        args = mock_model.generate_content_async.call_args[0]
        prompt = args[0]
        assert "TECHNICAL OBJECTIVE: Do X" in prompt

async def test_fundamentals_progression(db_session, curriculum_setup):
    """Verify a user who finished Q1 gets Q2."""
    # 1. Pre-complete Q1
    uq = UserQuest(user_id="student", source="fundamentals", quest_def_id="q1", status="completed")
    db_session.add(uq)
    await db_session.commit()
    
    track = {"id": "test-track", "name": "Test Track", "source": "fundamentals"}
    
    mock_model = MagicMock()
    mock_model.generate_content_async = AsyncMock(return_value=AsyncMock(__aiter__=lambda self: iter([])))

    async def mock_get_session():
        yield db_session

    mock_vertexai = MagicMock()
    mock_vertexai.generative_models.GenerativeModel = MagicMock(return_value=mock_model)

    with patch.dict(sys.modules, {"vertexai": mock_vertexai, "vertexai.generative_models": mock_vertexai.generative_models}), \
         patch("arcade_app.quest_helper.get_session", side_effect=mock_get_session):
        async for _ in stream_quest_generator("start", track, "student"):
            pass
            
        # Check DB for NEW Active Quest (Q2)
        uqs = (await db_session.execute(
            select(UserQuest).where(UserQuest.user_id == "student").order_by(UserQuest.created_at.desc())
        )).scalars().all()
        
        active_quest = next(q for q in uqs if q.status == "active")
        assert active_quest.quest_def_id == "q2"

async def test_track_completion(db_session, curriculum_setup):
    """Verify message when no quests remain."""
    # Pre-complete Q2 (Max sequence)
    uq = UserQuest(user_id="student", source="fundamentals", quest_def_id="q2", status="completed")
    db_session.add(uq)
    await db_session.commit()
    
    track = {"id": "test-track", "source": "fundamentals"}
    
    async def mock_get_session():
        yield db_session

    with patch("arcade_app.quest_helper.get_session", side_effect=mock_get_session):
        output = []
        async for chunk in stream_quest_generator("start", track, "student"):
            output.append(chunk)
        
        result = "".join(output)
        assert "TRACK COMPLETE" in result

async def test_dynamic_project_path(db_session, curriculum_setup):
    """Verify 'user-repo' source skips DB lookups and uses Repo Config."""
    track = {
        "id": "my-proj", 
        "source": "user-repo", 
        "repo_config": {"url": "http://github.com/me/code", "stack": ["python"]}
    }
    
    mock_model = MagicMock()
    mock_model.generate_content_async = AsyncMock(return_value=AsyncMock(__aiter__=lambda self: iter([])))

    mock_vertexai = MagicMock()
    mock_vertexai.generative_models.GenerativeModel = MagicMock(return_value=mock_model)

    with patch.dict(sys.modules, {"vertexai": mock_vertexai, "vertexai.generative_models": mock_vertexai.generative_models}):
        async for _ in stream_quest_generator("start", track, "student"):
            pass
            
        # Check Prompt for Dynamic Context
        args = mock_model.generate_content_async.call_args[0]
        prompt = args[0]
        assert "http://github.com/me/code" in prompt
        assert "refactor opportunity" in prompt
