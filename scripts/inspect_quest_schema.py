import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect
from arcade_app.database import engine
from sqlalchemy import text

async def inspect_schema():
    print("Inspecting 'quests' table schema...")
    
    # Use synchronous engine inspection if possible, or execute raw SQL
    # Since engine might be async, let's try raw SQL for postgres to list columns
    
    from arcade_app.database import get_session
    async for session in get_session():
        try:
            # Postgres specific query to list columns
            query = text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'quest';")
            result = await session.execute(query)
            columns = result.fetchall()
            
            if not columns:
                print("Table 'quest' not found (or empty result). Trying 'quests'...")
                query = text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'quests';")
                result = await session.execute(query)
                columns = result.fetchall()

            print(f"Found {len(columns)} columns:")
            found_tutorial = False
            for col in columns:
                print(f"- {col[0]} ({col[1]})")
                if col[0] == 'tutorial_md':
                    found_tutorial = True
            
            if found_tutorial:
                print("\n[SUCCESS] 'tutorial_md' column DOES exist.")
            else:
                print("\n[FAILURE] 'tutorial_md' column is MISSING.")
                
        except Exception as e:
            print(f"Error: {e}")
        break

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(inspect_schema())
