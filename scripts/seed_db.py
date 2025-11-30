import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import User, Profile
from sqlmodel import select

async def seed():
    print("🌱 Seeding Database...")
    
    # 1. Create Tables (Idempotent)
    await init_db()
    print("✅ Tables Created.")

    # 2. Seed Initial User
    async for session in get_session():
        # Check if 'leo' exists
        statement = select(User).where(User.id == "leo")
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        
        if not user:
            print("   + Creating User: leo")
            user = User(id="leo", name="Leo (Dev)")
            session.add(user)
            
            # Create empty profile
            profile = Profile(user_id="leo", total_xp=0, global_level=1)
            session.add(profile)
            
            await session.commit()
        else:
            print("   * User 'leo' already exists.")
            
    print("✨ Database Ready.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
