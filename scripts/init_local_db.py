"""
Quick script to initialize the local database schema.
This runs init_db() with a timeout to avoid hanging.
"""
import asyncio
import os
from arcade_app.database import init_db

async def main():
    print("🔧 Initializing database schema...")
    print(f"📍 DATABASE_URL: {os.getenv('DATABASE_URL', '(not set)')}")
    
    try:
        # Run with timeout
        await asyncio.wait_for(init_db(), timeout=30.0)
        print("✅ Database initialization complete!")
    except asyncio.TimeoutError:
        print("❌ Database initialization timed out after 30 seconds")
        print("   This usually means there's a lock or connection issue")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
