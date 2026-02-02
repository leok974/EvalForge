
import os
import sys
import subprocess
import json

# Local import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.universe import load_universe_map

def main():
    root_dir = os.getcwd()
    targets_path = os.path.join(root_dir, "artifacts", "world-python-tier2-targets.json")
    
    if not os.path.exists(targets_path):
        print(f"❌ Targets file not found: {targets_path}")
        return

    with open(targets_path, "r") as f:
        target_data = json.load(f)
        
    slugs = target_data.get("slugs", [])
    tier = target_data.get("tier", 2)
    universe = load_universe_map(root_dir)
    
    print(f"🎯 Found {len(slugs)} Tier-{tier} targets.")
    
    for slug in slugs:
        # Check if overlay already exists
        tut_path = os.path.join(root_dir, "docs", "quests", slug, "tutorial.md")
        if os.path.exists(tut_path):
            print(f"⏭️  Skipping {slug} (overlay exists)")
            continue

        print(f"\n🚀 Scaffolding {slug}...")
        meta = universe.get(slug)
        if not meta:
            print(f"⚠️  Metadata not found for {slug}, using defaults.")
            meta = {}
            
        cmd = [
            sys.executable, "scripts/quest_new.py",
            "--slug", slug,
            "--world", meta.get("world_slug", target_data.get("world_id", "world-python")),
            "--track", meta.get("track_id", "core"),
            "--title", meta.get("title", slug),
            "--with-tutorial",
            "--terms", "2", # Tier 2 Requirement
            "--codex-stubs"
        ]
        
        # print(" ".join(cmd))
        subprocess.run(cmd, check=False)
        
        # Post-process: Add example placeholder
        if os.path.exists(tut_path):
             with open(tut_path, "a", encoding="utf-8") as f:
                 f.write("\n\n### Example\n```python\n# TODO: Add tier-2 example\n```\n")
                 print("✅ Added tier-2 example stub.")

if __name__ == "__main__":
    main()
