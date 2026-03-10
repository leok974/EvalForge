import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.getcwd())

from arcade_app.config import DATABASE_URL
from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests

def main():
    sync_url = DATABASE_URL.replace("+asyncpg", "")
    print(f"Connecting to: {sync_url}")
    engine = create_engine(sync_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        print("🚀 Seeding standard quests...")
        seed_standard_world_quests(db)
        print("✅ Done.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
