from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from arcade_app.auth_helper import get_current_user
from arcade_app.skill_helper import get_skill_tree, unlock_skill

router = APIRouter(prefix="/api/skills", tags=["skills"])

class UnlockRequest(BaseModel):
    skill_id: str

@router.get("")
async def list_skills(
    current_user: Dict = Depends(get_current_user)
):
    """
    Returns a list of skills.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    return await get_skill_tree(current_user["id"])

@router.post("/unlock")
async def unlock_skill_endpoint(
    payload: UnlockRequest,
    current_user: Dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    result = await unlock_skill(current_user["id"], payload.skill_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result
