from fastapi import APIRouter, Depends, HTTPException
from arcade_app.auth_helper import get_current_user
from arcade_app.database import get_session
from arcade_app.models import BossDefinition, KnowledgeChunk, BossCodexProgress, Profile
from sqlmodel import select
from typing import List, Dict, Any

router = APIRouter(prefix="/api/codex/boss", tags=["boss_codex"])

@router.get("")
async def list_boss_codex(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    async for session in get_session():
        # Get Profile
        profile = (await session.exec(select(Profile).where(Profile.user_id == user["id"]))).first()
        if not profile:
            return {"bosses": []}

        # Get all active bosses
        bosses = (await session.exec(select(BossDefinition).where(BossDefinition.enabled == True))).all()
        
        # Get progress for this profile
        progress_stmt = select(BossCodexProgress).where(BossCodexProgress.profile_id == profile.id)
        progress_list = (await session.exec(progress_stmt)).all()
        progress_by_boss = {p.boss_id: p for p in progress_list}

        # Fetch all codex chunks
        # In a real app, we'd filter by metadata_json->>'boss_id' IS NOT NULL
        # For now, fetch all codex chunks and filter in python
        chunks = (await session.exec(select(KnowledgeChunk).where(KnowledgeChunk.source_type == "codex"))).all()
        
        response = []
        for boss in bosses:
            prog = progress_by_boss.get(boss.id)
            tier_unlocked = prog.tier_unlocked if prog else 0

            # Filter docs for this boss
            boss_docs = []
            for d in chunks:
                meta = d.metadata_json or {}
                if meta.get("boss_id") == boss.id:
                    boss_docs.append({
                        "slug": d.source_id, # Using source_id as slug for now
                        "title": meta.get("title", d.source_id),
                        "tier": int(meta.get("tier", 1))
                    })
            
            response.append({
                "boss_id": boss.id,
                "name": boss.name,
                "world_id": boss.world_id,
                "tier_unlocked": tier_unlocked,
                "docs": sorted(boss_docs, key=lambda m: m["tier"]),
                "kills": prog.wins if prog else 0,
                "deaths": prog.deaths if prog else 0,
            })

        return {"bosses": response}

@router.get("/{boss_id}")
async def get_boss_codex(boss_id: str, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async for session in get_session():
        profile = (await session.exec(select(Profile).where(Profile.user_id == user["id"]))).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        boss = await session.get(BossDefinition, boss_id)
        if not boss:
            raise HTTPException(status_code=404, detail="Boss not found")

        # Get progress
        prog_stmt = select(BossCodexProgress).where(
            BossCodexProgress.profile_id == profile.id,
            BossCodexProgress.boss_id == boss_id
        )
        prog = (await session.exec(prog_stmt)).first()
        tier_unlocked = prog.tier_unlocked if prog else 0

        # Get docs
        chunks = (await session.exec(select(KnowledgeChunk).where(KnowledgeChunk.source_type == "codex"))).all()
        
        docs_payload = []
        for d in chunks:
            meta = d.metadata_json or {}
            if meta.get("boss_id") == boss_id:
                tier = int(meta.get("tier", 1))
                is_unlocked = tier <= tier_unlocked
                
                docs_payload.append({
                    "slug": d.source_id,
                    "title": meta.get("title", d.source_id),
                    "tier": tier,
                    "unlocked": is_unlocked,
                    "body_md": d.content if is_unlocked else None
                })

        return {
            "boss": {
                "boss_id": boss.id,
                "name": boss.name,
                "world_id": boss.world_id,
                "tier_unlocked": tier_unlocked,
            },
            "docs": sorted(docs_payload, key=lambda x: x["tier"]),
        }
