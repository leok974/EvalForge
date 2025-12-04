from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from arcade_app.auth_helper import get_current_user
from arcade_app.database import get_session
from arcade_app.models import BossCodexProgress, BossDefinition
from arcade_app.boss_helper import create_encounter
from sqlmodel import select, delete

router = APIRouter(prefix="/api/dev", tags=["dev"])

class ForceBossRequest(BaseModel):
    boss_id: str

@router.post("/force_boss")
async def force_boss(req: ForceBossRequest, user=Depends(get_current_user)):
    """
    Dev endpoint to force spawn a specific boss encounter.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Verify boss exists
    async for session in get_session():
        print(f"DEBUG: force_boss engine: {session.bind.url}")
        print(f"DEBUG: force_boss looking for {req.boss_id}")
        boss = await session.get(BossDefinition, req.boss_id)
        print(f"DEBUG: force_boss found: {boss}")
        if not boss:
            raise HTTPException(status_code=404, detail=f"Boss {req.boss_id} not found")
        break

    # Create encounter
    enc = await create_encounter(user["id"], req.boss_id)
    
    # Emit FX
    from arcade_app.socket_manager import emit_fx_event
    await emit_fx_event(user["id"], {
        "type": "boss_spawn",
        "boss_id": enc.boss_id,
        "severity": "high",
    })
    
    return {
        "status": "spawned",
        "encounter_id": enc.id,
        "boss_id": enc.boss_id
    }

@router.delete("/boss_codex/{boss_id}")
async def reset_boss_progress(boss_id: str, user=Depends(get_current_user)):
    """
    Dev endpoint to reset codex progress for a specific boss.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async for session in get_session():
        # Delete BossCodexProgress
        stmt = delete(BossCodexProgress).where(
            BossCodexProgress.user_id == user["id"],
            BossCodexProgress.boss_id == boss_id
        )
        await session.exec(stmt)
        await session.commit()
        
    return {"status": "reset", "boss_id": boss_id}

