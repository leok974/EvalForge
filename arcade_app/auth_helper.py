import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwt, JWTError
from fastapi import Request, Response
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import User, Profile

# Config
AUTH_MODE = os.getenv("EVALFORGE_AUTH_MODE", "mock")
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

# --- 1. OAUTH LOGIC ---

def get_login_url() -> str:
    if AUTH_MODE == "mock":
        return "/api/auth/github/callback?code=mock_code" # Short-circuit for dev
    
    return (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&scope=read:user"
    )

async def exchange_github_code(code: str) -> Dict:
    """Exchanges the temporary code for a GitHub Access Token."""
    async with httpx.AsyncClient() as client:
        # 1. Exchange Code
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code
            }
        )
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise ValueError("Failed to retrieve access token from GitHub")

        # 2. Get User Profile
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return user_res.json()

# --- 2. USER MANAGEMENT ---

async def get_or_create_github_user(gh_user: Dict) -> User:
    """Upserts the GitHub user into our Postgres DB."""
    user_id = gh_user["login"].lower()
    
    async for session in get_session():
        # Check if exists
        user = await session.get(User, user_id)
        
        if not user:
            # Create User
            user = User(
                id=user_id,
                name=gh_user.get("name") or user_id,
                avatar_url=gh_user.get("avatar_url")
            )
            session.add(user)
            
            # Create Profile
            profile = Profile(user_id=user_id)
            session.add(profile)
            
            await session.commit()
            await session.refresh(user)
        else:
            # Update metadata if changed
            if user.avatar_url != gh_user.get("avatar_url"):
                user.avatar_url = gh_user.get("avatar_url")
                session.add(user)
                await session.commit()
                
        return user

# --- 3. SESSION MANAGEMENT (JWT) ---

def create_session_token(user_id: str) -> str:
    """Mint a JWT for the user."""
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request) -> Dict:
    """
    Dependency to get the current user from the Session Cookie.
    """
    # 1. Mock Fallback
    if AUTH_MODE == "mock":
        # (Same mock logic as before for dev safety)
        async for session in get_session():
            user = await session.get(User, "leo")
            if user:
                return {
                    "id": user.id,
                    "name": user.name,
                    "avatar_url": user.avatar_url or "",
                    "current_avatar_id": user.current_avatar_id or "default_user",
                    "auth_mode": "mock"
                }
            return {}

    # 2. Real JWT Check
    token = request.cookies.get("session_token")
    if not token:
        return {}

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id:
            async for session in get_session():
                user = await session.get(User, user_id)
                # Ensure we return the full object including avatar relation manually if needed
                # For now .dict() is fine, frontend handles the rest
                if user:
                    return {
                        "id": user.id,
                        "name": user.name,
                        "avatar_url": user.avatar_url,
                        "current_avatar_id": user.current_avatar_id,
                        "auth_mode": "github"
                    }
    except JWTError:
        pass
        
    return {}
