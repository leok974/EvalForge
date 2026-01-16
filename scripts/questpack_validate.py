
import json
import sys
import os
import re
from pathlib import Path

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def validate_quest_pack(file_path):
    print(f"Validating {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
        return False
        
    if not isinstance(data, list):
         print("❌ Root element must be a list of quest objects.")
         return False
         
    # Load universe data for references
    worlds = set()
    tracks = set()
    try:
        if os.path.exists("data/worlds.json"):
            with open("data/worlds.json", "r") as f:
                worlds = {w["id"] for w in json.load(f)}
        if os.path.exists("data/tracks.json"):
            with open("data/tracks.json", "r") as f:
                tracks = {t["id"] for t in json.load(f)}
    except:
        print("⚠️ Warning: Could not load universe data. Skipping reference checks.")

    all_ok = True
    seen_ids = set()
    seen_slugs = set()

    for i, quest in enumerate(data):
        q_id = quest.get("id") or f"index_{i}"
        slug = quest.get("slug")
        print(f"  Checking {q_id} ({slug})...")
        
        # Required Fields
        required = ["slug", "world_id", "track_id", "title", "starter_code", "language"]
        missing = [f for f in required if not quest.get(f)]
        if missing:
            print(f"    ❌ Missing required fields: {missing}")
            all_ok = False
            
        # Duplicates
        if slug in seen_slugs:
            print(f"    ❌ Duplicate slug: {slug}")
            all_ok = False
        seen_slugs.add(slug)
        
        # References
        if worlds and quest.get("world_id") not in worlds:
             print(f"    ❌ Unknown world_id: {quest.get('world_id')}")
             all_ok = False
        if tracks and quest.get("track_id") not in tracks:
             print(f"    ❌ Unknown track_id: {quest.get('track_id')}")
             all_ok = False
             
        # Objectives
        objs = quest.get("objectives", [])
        if not objs:
            print("    ⚠️ No objectives defined.")
        
        seen_obj_ids = set()
        for idx, obj in enumerate(objs):
            oid = obj.get("id")
            if not oid:
                print(f"    ❌ Objective #{idx} missing ID")
                all_ok = False
            elif oid in seen_obj_ids:
                 print(f"    ❌ Duplicate objective ID: {oid}")
                 all_ok = False
            seen_obj_ids.add(oid)
            
            kind = obj.get("kind")
            rule = obj.get("rule")
            if not kind:
                 print(f"    ❌ Objective {oid} missing kind")
                 all_ok = False
                 
            # Regex check
            if kind == "stdout_regex" and rule:
                pat = rule.get("pattern")
                try:
                    re.compile(pat)
                except:
                     print(f"    ❌ Invalid regex pattern in {oid}: {pat}")
                     all_ok = False

        # Hints
        hints = quest.get("tiered_hints", {})
        if not hints.get("concept") or not hints.get("guided") or not hints.get("full_solution"):
             print("    ❌ Missing tiered hints (concept/guided/full_solution)")
             all_ok = False
             
        # Runtime Rules
        rt = quest.get("runtime", {})
        if rt.get("enabled"):
             if rt.get("timeout_ms", 0) > 30000:
                 print("    ⚠️ Timeout > 30s seems high.")
                 
    return all_ok

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python questpack_validate.py <path_to_json>")
        sys.exit(1)
        
    path = sys.argv[1]
    if validate_quest_pack(path):
        print("\n✅ Validation Passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation Failed.")
        sys.exit(1)
