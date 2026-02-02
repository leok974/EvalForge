
import os
import sys
import subprocess
import json
import argparse

# Local import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.universe import load_universe_map

def main():
    parser = argparse.ArgumentParser(description="Scaffold missing quests based on a manifest.")
    parser.add_argument("--world", required=True, help="World ID (e.g., world-js)")
    parser.add_argument("--tier", type=int, required=True, help="Target Tier (1 or 2)")
    parser.add_argument("--manifest", required=True, help="Path to targets manifest JSON")
    args = parser.parse_args()

    root_dir = os.getcwd()
    manifest_path = os.path.join(root_dir, args.manifest)
    
    if not os.path.exists(manifest_path):
        print(f"❌ Manifest not found: {manifest_path}")
        return

    with open(manifest_path, "r") as f:
        target_data = json.load(f)
        
    slugs = target_data.get("slugs", [])
    tier = args.tier
    world = args.world
    
    print(f"🎯 Found {len(slugs)} Tier-{tier} targets for {world}.")
    
    universe = load_universe_map(root_dir)

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
            "--world", meta.get("world_slug", world),
            "--track", meta.get("track_id", "core"), # Default track
            "--title", meta.get("title", slug),
            "--with-tutorial",
            "--terms", "3" if tier == 1 else "2", # Stricter terms for Tier 1
            "--codex-stubs"
        ]
        
        # print(" ".join(cmd))
        subprocess.run(cmd, check=False)
        
        # Post-process: Add example placeholder or structure
        if os.path.exists(tut_path):
             with open(tut_path, "a", encoding="utf-8") as f:
                 if tier == 1:
                     f.write("\n\n### Example\n```javascript\n// Tier-1 Strict Example Required\nconsole.log('Hello');\n```\n")
                 else:
                     f.write("\n\n### Example\n```javascript\n// TODO: Add tier-2 example\n```\n")
                 print(f"✅ Added Tier-{tier} example stub.")

if __name__ == "__main__":
    main()
