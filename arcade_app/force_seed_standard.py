import sys
import os
import time

sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from arcade_app.models import QuestDefinition
from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests
from arcade_app.config import DATABASE_URL

# Inline content for missing files
STARTER_CONTENT = {
    # Python
    "python-ignition": """# Quest: Ignition
# Objective: Print a status line.

def main():
    # TODO: Define variables for system name and status
    system_name = "..."
    status = "..."
    
    # TODO: Print the formatted string f"System {system_name}: {status}"
    pass

if __name__ == "__main__":
    main()
""",
    "python-loop": """# Quest: Loop
# Objective: Process a list of sensor readings.

readings = [12, 45, 0, 99, -5, 23]

def process_readings(data):
    # TODO: Loop through data
    # TODO: Filter out negative values
    # TODO: Return the count of valid readings
    return 0

if __name__ == "__main__":
    print(process_readings(readings))
""",
    "python-data-forge": """# Quest: Data Forge
# Objective: Parse raw data into a structured format.

raw_data = [
    {"id": "A1", "val": "100"},
    {"id": "B2", "val": "invalid"},
    {"id": "C3", "val": "50"}
]

def forge(data):
    # TODO: Parse 'val' as int. specialized handling for errors.
    # Return list of valid dicts.
    return []

if __name__ == "__main__":
    print(forge(raw_data))
"""
}

def inject_starter_code(db):
    print("💉 Injecting starter code...")
    for slug, content in STARTER_CONTENT.items():
        q = db.query(QuestDefinition).filter(QuestDefinition.slug == slug).first()
        if q:
            q.starter_code = content
            # Also clear the path so it doesn't confuse logic
            # q.starting_code_path = None 
            db.add(q)
            print(f"   - Injected code for {slug}")
        else:
            print(f"   ⚠️ Quest {slug} not found in DB")
    db.commit()

if __name__ == "__main__":
    print("🚀 Force Seeding Standard Questlines (Sync Mode + Content Injection)...")
    try:
        sync_url = DATABASE_URL.replace("+asyncpg", "")
        print(f"   Connecting to: {sync_url}")
        
        engine = create_engine(sync_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()
        try:
            # 1. Ensure Quests Exist
            seed_standard_world_quests(db)
            
            # 2. Inject Content
            inject_starter_code(db)
            print("✅ Standard Questlines Seeded & Content Injected.")
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            raise e
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
