import sys
import os
from pathlib import Path

# Add project root to path to import arcade_app
sys.path.append(os.getcwd())

try:
    from arcade_app.seed_quests_standard_worlds import STANDARD_QUESTLINES
except ImportError as e:
    print(f"❌ Failed to import STANDARD_QUESTLINES: {e}")
    sys.exit(1)

def main():
    print("🔍 Verifying Standard Quest Seed Paths...")
    failures = []
    
    for cfg in STANDARD_QUESTLINES:
        slug = cfg.get("slug", "unknown")
        code_path = cfg.get("starting_code_path")
        
        if not code_path:
            # Some quests might not have starter code (e.g. pure quiz?)
            # But usually they do in this list.
            # Warn?
            continue
            
        # Path is relative to project root usually
        full_path = Path(code_path)
        
        if not full_path.exists():
            failures.append(f"[{slug}] Missing starting_code_path: {code_path}")
            
    if failures:
        print(f"❌ Found {len(failures)} path errors in seed config:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"✅ Verified {len(STANDARD_QUESTLINES)} quests in seed config. All paths exist.")
        
if __name__ == "__main__":
    main()
