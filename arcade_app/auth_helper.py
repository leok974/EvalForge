import os
from typing import Dict, Any

MOCK_USER = {
    "id": "leo",
    "name": "Leo (Dev)",
    "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
    "auth_mode": "mock"
}

def get_current_user() -> Dict[str, Any]:
    # In real mode, verify JWT/Session
    if os.getenv("EVALFORGE_AUTH_MODE", "mock") == "mock":
        return MOCK_USER
    return {} # Return empty if not logged in
