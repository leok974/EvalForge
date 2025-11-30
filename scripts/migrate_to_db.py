import asyncio
import json
import os
from sqlmodel import select
from arcade_app.database import engine, init_db, get_session
from arcade_app.models import User, Profile, Project

async def migrate():
    print("🚀 Starting Migration...")
    await init_db()
    
    async_session = get_session()
    async for session in async_session:
        try:
            # 1. Migrate Profiles (Users)
            if os.path.exists("data/profiles.json"):
                with open("data/profiles.json", "r") as f:
                    profiles_data = json.load(f)
                
                for user_id, p_data in profiles_data.items():
                    print(f"Migrating User: {user_id}")
                    
                    # Ensure User exists
                    user = await session.get(User, user_id)
                    if not user:
                        user = User(id=user_id, name=f"{user_id.capitalize()} (Migrated)")
                        session.add(user)
                    
                    # Ensure Profile exists
                    # Check if profile exists via relationship or query
                    # For simplicity, query by user_id
                    stmt = select(Profile).where(Profile.user_id == user_id)
                    result = await session.exec(stmt)
                    profile = result.first()
                    
                    if not profile:
                        profile = Profile(
                            user_id=user_id,
                            total_xp=p_data.get("total_xp", 0),
                            global_level=p_data.get("level", 1),
                            world_progress=p_data.get("world_progress", {}),
                            recent_badges=p_data.get("recent_badges", [])
                        )
                        session.add(profile)
                    else:
                        # Update existing
                        profile.total_xp = p_data.get("total_xp", 0)
                        profile.global_level = p_data.get("level", 1)
                        profile.world_progress = p_data.get("world_progress", {})
                        session.add(profile)
            
            # 2. Migrate Projects
            if os.path.exists("data/projects.json"):
                with open("data/projects.json", "r") as f:
                    projects_data = json.load(f)
                
                for proj in projects_data:
                    print(f"Migrating Project: {proj['name']}")
                    
                    # Ensure Owner exists (if not in profiles)
                    owner_id = proj["owner_user_id"]
                    owner = await session.get(User, owner_id)
                    if not owner:
                        owner = User(id=owner_id, name=f"{owner_id} (Project Owner)")
                        session.add(owner)
                    
                    # Upsert Project
                    db_proj = await session.get(Project, proj["id"])
                    if not db_proj:
                        db_proj = Project(
                            id=proj["id"],
                            owner_user_id=owner_id,
                            name=proj["name"],
                            repo_url=proj["repo_url"],
                            provider=proj.get("provider", "github"),
                            source=proj.get("source", "user"),
                            default_world_id=proj.get("default_world_id", "world-infra"),
                            summary_data=proj.get("summary", {}),
                            sync_status=proj.get("sync_status", "pending"),
                            last_sync_at=None # Parse string if needed
                        )
                        session.add(db_proj)
            
            await session.commit()
            print("✅ Migration Complete!")
            
        except Exception as e:
            print(f"❌ Migration Failed: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(migrate())
