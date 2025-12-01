from typing import List, Dict
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import SkillNode, UserSkill, User, Profile

async def get_skill_tree(user_id: str) -> Dict:
    """Returns full tree + user's unlock status + SP balance."""
    async for session in get_session():
        # 1. Get User Profile (for SP)
        # Fix: Profile ID is int, user_id is string. Need lookup.
        p_res = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = p_res.scalars().first()
        
        sp = profile.skill_points if profile else 0

        # 2. Get All Skills
        all_skills_res = await session.execute(select(SkillNode))
        all_skills = all_skills_res.scalars().all()
        
        # 3. Get Unlocked
        unlocked_res = await session.execute(select(UserSkill).where(UserSkill.user_id == user_id))
        unlocked_ids = {u.skill_id for u in unlocked_res.scalars().all()}

        # 4. Build Response
        nodes = []
        for s in all_skills:
            # Can Unlock Logic:
            # 1. Not already unlocked
            # 2. Has enough points
            # 3. Parent is unlocked (or no parent)
            parent_ok = (s.parent_id is None) or (s.parent_id in unlocked_ids)
            can_unlock = (s.id not in unlocked_ids) and (sp >= s.cost) and parent_ok
            
            nodes.append({
                **s.dict(),
                "is_unlocked": s.id in unlocked_ids,
                "can_unlock": can_unlock
            })
            
        return {"skill_points": sp, "nodes": nodes}

async def unlock_skill(user_id: str, skill_id: str) -> Dict:
    async for session in get_session():
        # 1. Fetch Data
        skill = await session.get(SkillNode, skill_id)
        if not skill: return {"error": "Skill not found"}
        
        p_res = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = p_res.scalars().first()
        if not profile: return {"error": "Profile not found"}

        # 2. Checks
        # Already unlocked?
        existing_res = await session.execute(select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id))
        if existing_res.scalars().first(): return {"status": "already_unlocked"}

        # Points?
        if profile.skill_points < skill.cost:
            return {"error": "Insufficient Skill Points"}

        # Parent?
        if skill.parent_id:
            parent_check_res = await session.execute(select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill.parent_id))
            if not parent_check_res.scalars().first():
                return {"error": "Dependency not met (Unlock parent first)"}

        # 3. Transact
        profile.skill_points -= skill.cost
        unlock = UserSkill(user_id=user_id, skill_id=skill_id)
        
        session.add(profile)
        session.add(unlock)
        await session.commit()
        
        return {"status": "ok", "remaining_sp": profile.skill_points}
