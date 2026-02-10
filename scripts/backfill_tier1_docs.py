#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

# Config
QUESTPACKS_DIR = Path("data/questpacks")
SCAFFOLD_SCRIPT = "scripts/scaffold_quest_docs.py"

def main():
    print("🚀 Starting Tier-1 Docs Backfill...")
    
    # 1. Gather all Tier-1 quests
    tier1_slugs = []
    
    for qp_file in QUESTPACKS_DIR.glob("*.json"):
        try:
            data = json.loads(qp_file.read_text(encoding="utf-8"))
            quests = []
            
            if isinstance(data, list):
                quests = data
            elif isinstance(data, dict):
                quests = data.get("quests", [])
            
            if not isinstance(quests, list):
                continue
                
            for q in quests:
                # Check tier (default to 1 if missing for now, to ensure backfill happens)
                tier = q.get("tutorial_tier") or q.get("tier") or 0
                if isinstance(q.get("meta"), dict):
                     tier = q.get("meta", {}).get("tutorial_tier", tier)
                
                # Force Tier-1 for core packs if unspecified
                if tier == 0:
                    tier = 1
                
                if tier >= 1:
                    slug = q.get("slug")
                    if slug:
                        tier1_slugs.append((slug, tier))
                        
        except Exception as e:
            print(f"⚠️  Error reading {qp_file}: {e}")

    print(f"📋 Found {len(tier1_slugs)} Tier-1+ quests.")
    
    # 2. Run scaffolder for each
    for slug, tier in tier1_slugs:
        print(f"👉 Scaffolding {slug} (Tier {tier})...")
        cmd = [
            sys.executable, 
            SCAFFOLD_SCRIPT, 
            "--slug", slug, 
            "--tier", str(tier),
            "--with-lore"
        ]
        
        # Check existing tutorial for placeholder content
        tut_path = Path("docs/quests") / slug / "tutorial.md"
        if tut_path.exists():
            content = tut_path.read_text(encoding="utf-8")
            if "The Concept in 30 Seconds" in content or "term 1" in content or "term 2" in content:
                print(f"👉 Force updating placeholder content for {slug}")
                cmd.append("--force")
        
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to scaffold {slug}: {e}")

    print("\n✅ Backfill Complete.")

if __name__ == "__main__":
    main()
