import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import User, Profile

async def seed_user():
    print("👤 Seeding Default User (leo)...")
    await init_db()
    
    async for session in get_session():
        user_id = "leo"
        
        # Check if exists
        user = await session.get(User, user_id)
        if not user:
            user = User(
                id=user_id,
                name="Leo (Dev)",
                avatar_url="https://github.com/leok974.png",
                current_avatar_id="default_user"
            )
            session.add(user)
            
            # Create Profile
            profile = Profile(user_id=user_id)
            session.add(profile)
            
            await session.commit()
            print("✅ Created User: leo")
        else:
            print("ℹ️ User 'leo' already exists.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_user())
