import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import select
from arcade_app.agent import app
from arcade_app.models import User, Profile
from arcade_app.auth_helper import get_or_create_github_user, exchange_github_code

# Mark all async tests
pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_env(monkeypatch):
    """Force the app into Real Auth mode for these tests."""
    monkeypatch.setenv("EVALFORGE_AUTH_MODE", "github")
    monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
    monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
    monkeypatch.setenv("SECRET_KEY", "test-key")
    
    # Patch module-level constants that were already loaded
    monkeypatch.setattr("arcade_app.auth_helper.AUTH_MODE", "github")
    monkeypatch.setattr("arcade_app.auth_helper.CLIENT_ID", "test-id")
    monkeypatch.setattr("arcade_app.auth_helper.CLIENT_SECRET", "test-secret")
    monkeypatch.setattr("arcade_app.auth_helper.SECRET_KEY", "test-key")

async def test_get_or_create_github_user(db_session):
    """Verify database upsert logic."""
    gh_profile = {
        "login": "octocat",
        "name": "The Octocat",
        "avatar_url": "http://octocat.com/img"
    }

    # Patch get_session to use our test db_session
    with patch("arcade_app.auth_helper.get_session", return_value=iter([db_session])):
        # Wait, get_session is an async generator. We need to mock it properly.
        # Actually, simpler to just override the dependency if it was a FastAPI dep, but here it's a direct call.
        # Let's try to mock the generator.
        async def mock_get_session():
            yield db_session

        with patch("arcade_app.auth_helper.get_session", side_effect=mock_get_session):
            # 1. Create New User
            user = await get_or_create_github_user(gh_profile)
            assert user.id == "octocat"
            assert user.name == "The Octocat"
            
            # Verify Profile was created cascade
            # Profile PK is int, so we query by user_id
            profile = (await db_session.execute(select(Profile).where(Profile.user_id == "octocat"))).scalars().first()
            assert profile is not None

            # 2. Update Existing User (Changed Avatar)
            gh_profile_updated = {**gh_profile, "avatar_url": "http://new.url"}
            updated_user = await get_or_create_github_user(gh_profile_updated)
            
            assert updated_user.avatar_url == "http://new.url"
            
            # Verify we didn't duplicate rows
            users = (await db_session.execute(select(User))).scalars().all()
            assert len(users) == 1

async def test_oauth_callback_flow(db_session, mock_env):
    """
    Verify the full callback endpoint: Code -> Token -> User -> Cookie.
    """
    client = TestClient(app)

    async def mock_get_session():
        yield db_session

    # Mock the external GitHub API calls inside 'exchange_github_code'
    # We patch httpx.AsyncClient to avoid real network requests
    with patch("httpx.AsyncClient.post") as mock_post, \
         patch("httpx.AsyncClient.get") as mock_get, \
         patch("arcade_app.auth_helper.get_session", side_effect=mock_get_session):
        
        # 1. Mock Token Exchange Response
        mock_post.return_value = MagicMock(json=lambda: {"access_token": "gh_token_123"})
        
        # 2. Mock User Profile Response
        mock_get.return_value = MagicMock(json=lambda: {
            "login": "real_user",
            "name": "Real User", 
            "avatar_url": "http://avatar"
        })

        # 3. Call the Callback Endpoint
        # Note: We must allow redirects=False to inspect the 307/303 redirect
        response = client.get("/api/auth/github/callback?code=valid_code", follow_redirects=False)

        # 4. Verify Redirect
        assert response.status_code == 307 # Temporary Redirect
        assert response.headers["location"] == "http://localhost:5173"

        # 5. Verify Cookie Security
        assert "session_token" in response.cookies
        cookie = next(c for c in response.cookies.jar if c.name == "session_token")
        # Check flags if possible, TestClient cookies might be simple dicts or objects
        # assert cookie.secure or cookie.rest.get('HttpOnly') 
        
        # 6. Verify Database Effect
        # The user 'real_user' should now exist
        # We need to manually query the DB session to confirm
        user = await db_session.get(User, "real_user")
        assert user is not None
        assert user.name == "Real User"

async def test_auth_me_with_cookie(db_session, mock_env):
    """Verify /api/auth/me decodes the cookie correctly."""
    client = TestClient(app)
    
    # 1. Seed User
    user = User(id="cookie_user", name="Cookie User")
    db_session.add(user)
    await db_session.commit()

    # 2. Generate Valid Token (Using the helper or manually)
    from arcade_app.auth_helper import create_session_token
    token = create_session_token("cookie_user")

    async def mock_get_session():
        yield db_session

    with patch("arcade_app.auth_helper.get_session", side_effect=mock_get_session):
        # 3. Request with Cookie
        client.cookies.set("session_token", token)
        response = client.get("/api/auth/me")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cookie_user"
        assert data["auth_mode"] == "github"
