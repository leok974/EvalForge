import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath('.'))

from sqlmodel import Session
from arcade_app.database import engine
from arcade_app.routers.routes_workshop import get_workshop_catalog

async def main():
    async with engine.begin() as conn:
        pass
        
    print("Testing /api/workshop/catalog directly...")
    
    from arcade_app.database import get_session
    
    # We need a session, so we can try to call it bypassing Depends
    async for session in get_session():
        try:
            res = await get_workshop_catalog(session=session, user_data={"id": "mock"})
            print(f"Returned {len(res['worlds'])} worlds and {len(res['tracks'])} tracks.")
            world_ids = [w['world_id'] for w in res['worlds']]
            print(f"Worlds: {world_ids}")
            break
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
