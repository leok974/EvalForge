import asyncio
from arcade_app.database import engine
from sqlmodel import select, Session
from arcade_app.models import QuestProgress, Profile, User, QuestDefinition

async def check_status():
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    # Manually create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # 1. Check User
        # In mock mode, user is 'leo'.
        user_id = 'leo'
        print(f"Checking for user: {user_id}")
        
        # 2. Check Profile
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = result.scalars().first()
        if not profile:
            print("Profile NOT FOUND!")
        else:
            print(f"Profile Found: {profile.id}, XP: {profile.total_xp}")
            
        # 3. List All Quests
        print("--- Listing All Quests ---")
        result_all = await session.execute(select(QuestDefinition))
        quests = result_all.scalars().all()
        for q in quests:
            print(f"[{q.id}] {q.slug} ('{q.title}')")
            
        print("--------------------------")

        # 4. Check Progress for Starter
        # ... logic if exists ...

if __name__ == "__main__":
    asyncio.run(check_status())
