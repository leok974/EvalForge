import sys
import os

# Ensure arcade_app is in path
sys.path.append(os.getcwd())

from arcade_app.database import SessionLocal
from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests

if __name__ == "__main__":
    print("🚀 Force Seeding Standard Questlines...")
    try:
        # Create sync session using SessionLocal
        # Note: seed_quests_standard_worlds uses a synchronous session signature (db: Session)
        db = SessionLocal()
        seed_standard_world_quests(db)
        print("✅ Standard Questlines Seeded Successfully.")
    except Exception as e:
        print(f"❌ Error seeding standard quests: {e}")
        import traceback
        traceback.print_exc()
