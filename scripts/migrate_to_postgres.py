import asyncio
import json
import os
import sys

# Add root to path so we can import arcade_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from arcade_app.database import engine, init_db
from arcade_app.models import User, Profile, Project
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# Paths to legacy data
PROFILES_FILE = "data/profiles.json"
PROJECTS_FILE = "data/projects.json"

async def migrate():
    print("🔄 Starting Migration to Postgres...")
    
    # 1. Initialize Tables
    await init_db()
    print("✅ Database Tables Created.")

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 2. Migrate Users & Profiles
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, "r") as f:
                profiles_data = json.load(f)
            
            for user_id, p_data in profiles_data.items():
                # Create User if not exists
                user = await session.get(User, user_id)
                if not user:
                    user = User(id=user_id, name=f"{user_id.capitalize()} (Legacy)")
                    session.add(user)
                    print(f"   + Created User: {user_id}")
                
                # Create/Update Profile
                # Check if profile exists via relationship is tricky in async without eager load
                # Simple check: query profile by user_id
                result = await session.exec(select(Profile).where(Profile.user_id == user_id))
                existing_profile = result.first()
                
                if not existing_profile:
                    profile = Profile(
                        user_id=user_id,
                        total_xp=p_data.get("total_xp", 0),
                        global_level=p_data.get("level", 1),
                        world_progress=p_data.get("world_progress", {})
                    )
                    session.add(profile)
                    print(f"   + Created Profile for {user_id}: {profile.total_xp} XP")
        else:
            print("⚠️ No profiles.json found. Skipping.")

        # 3. Migrate Projects
        if os.path.exists(PROJECTS_FILE):
            with open(PROJECTS_FILE, "r") as f:
                projects_data = json.load(f)
            
            for p_data in projects_data:
                # Ensure owner exists (e.g. if projects.json has user not in profiles.json)
                owner_id = p_data.get("owner_user_id", "leo")
                owner = await session.get(User, owner_id)
                if not owner:
                    owner = User(id=owner_id, name="Leo (Legacy Project Owner)")
                    session.add(owner)
                
                # Check if project exists
                p_id = p_data.get("id")
                existing_proj = await session.get(Project, p_id)
                
                if not existing_proj:
                    proj = Project(
                        id=p_id,
                        owner_user_id=owner_id,
                        name=p_data.get("name"),
                        repo_url=p_data.get("repo_url"),
                        provider=p_data.get("provider", "github"),
                        source=p_data.get("source", "user"),
                        default_world_id=p_data.get("default_world_id", "world-python"),
                        summary_data=p_data.get("summary", {}),
                        sync_status=p_data.get("sync_status", "pending"),
                        # Parse date string if exists, else None
                        last_sync_at=None 
                    )
                    session.add(proj)
                    print(f"   + Created Project: {proj.name}")
        else:
            print("⚠️ No projects.json found. Skipping.")

        await session.commit()
    
    print("✨ Migration Complete!")

if __name__ == "__main__":
    asyncio.run(migrate())
