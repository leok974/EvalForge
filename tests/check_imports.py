
import sys
import os

# Add root to pythonpath
sys.path.append("d:\\EvalForge")

print("Checking imports...")
try:
    from arcade_app.models import QuestDefinition
    print("✅ arcade_app.models imported")
    
    from arcade_app.progress_models import QuestProgressV2
    print("✅ arcade_app.progress_models imported")
    
    from arcade_app.routers import routes_quests
    print("✅ arcade_app.routers.routes_quests imported")
    
    from arcade_app.quest_helper import quest_to_dict
    print("✅ arcade_app.quest_helper imported")
    
    from arcade_app.progress_helper import compute_track_progress_for_user
    print("✅ arcade_app.progress_helper imported")

    print("All critical imports checked.")
except Exception as e:
    print(f"❌ Import Failed: {e}")
    sys.exit(1)
