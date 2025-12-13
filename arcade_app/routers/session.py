from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from arcade_app.auth_helper import get_current_user
from arcade_app.session_helper import get_or_create_session

router = APIRouter(prefix="/api/session", tags=["session"])

@router.get("/active")
async def get_active_session(
    current_user: Dict = Depends(get_current_user)
):
    """
    Returns the active session for the current user.
    """
    if not current_user:
        return {} # Or raise 401, but frontend might handle empty gracefully
        
    session_data = await get_or_create_session(current_user["id"])
    return session_data
