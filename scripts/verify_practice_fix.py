
import sys
import os

# Add project root to sys.path
sys.path.insert(0, r"d:\EvalForge")

try:
    print("Attempting to import arcade_app.practice_gauntlet...")
    import arcade_app.practice_gauntlet
    print("Successfully imported arcade_app.practice_gauntlet")
except Exception as e:
    print(f"Failed to import: {e}")
    import traceback
    traceback.print_exc()
