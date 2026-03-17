import json
import requests
import os
from pathlib import Path
import sys

# --- Configuration Loading ---
SCOPE_PATH = Path("configs/curriculum_guardrail_scope.json")
EXCLUSIONS_PATH = Path("configs/quest_exclusions.json")

def load_json(path, default):
    if not path.exists(): return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

SCOPE = load_json(SCOPE_PATH, {})
EXCLUSIONS = load_json(EXCLUSIONS_PATH, {}).get("excluded_slugs", [])

def is_active(slug, quest_data=None):
    if slug in EXCLUSIONS: return False
    
    # If we have quest_data (from JSON), we can check world/track
    if quest_data:
        world_id = quest_data.get("world_id")
        track_id = quest_data.get("track_id")
        if world_id in SCOPE.get("active_worlds", []): return True
        if track_id in SCOPE.get("active_tracks", []): return True
    
    # Fallback to general slug-based active check if needed, 
    # but usually we want to know if it's in an active world.
    return False

def audit_population():
    print("--- EvalForge Population Audit ---")
    
    # 1. Source (JSON)
    json_quests = {} # slug -> data
    root = Path("data/questpacks")
    for f in root.rglob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as jf:
                d = json.load(jf)
                qs = d if isinstance(d, list) else d.get("quests", [])
                for q in qs:
                    slug = q.get("slug") or q.get("quest_id")
                    if slug:
                        json_quests[slug] = q
        except: continue
    
    print(f"Source (JSON) Quests: {len(json_quests)}")
    
    # 2. DB / API (Requires backend running)
    global_errors = []
    active_errors = []
    warnings = []
    
    try:
        r = requests.get("http://localhost:8092/api/quests", timeout=5)
        api_quests = {q["slug"] for q in r.json()}
        print(f"API-Visible Quests:   {len(api_quests)}")
        
        json_slugs = set(json_quests.keys())
        missing_in_api = json_slugs - api_quests
        phantom_in_api = api_quests - json_slugs
        
        # Filter exclusions
        missing_in_api = {s for s in missing_in_api if s not in EXCLUSIONS}
        phantom_in_api = {s for s in phantom_in_api if s not in EXCLUSIONS}

        if missing_in_api:
            for slug in missing_in_api:
                q_data = json_quests.get(slug)
                q_active = is_active(slug, q_data)
                msg = f"Missing in API: {slug}"
                if q_active:
                    active_errors.append(msg)
                else:
                    warnings.append(msg)

        if phantom_in_api:
            for slug in phantom_in_api:
                # We don't have JSON data for phantoms, so we check if they belong to active worlds via track/world if possible?
                # For now, phantoms represent objects in DB not in source, which is usually a GLOBAL structural/sync issue.
                global_errors.append(f"Phantom in API (ghost quest): {slug}")
            
    except Exception as e:
        print(f"❌ Could not reach API: {e}")
        # Failing to reach API during a population audit is a GLOBAL fail
        sys.exit(1)

    # --- REPORTING ---
    if warnings:
        print(f"\n🟡 WARNINGS (Non-Active Missing): {len(warnings)}")
        for w in warnings[:10]: print(f"  - {w}")
        if len(warnings) > 10: print(f"  ... and {len(warnings)-10} more")
            
    if active_errors:
        print(f"\n🔴 FAIL (Active Scope Missing): {len(active_errors)}")
        for e in active_errors: print(f"  - {e}")
        
    if global_errors:
        print(f"\n💀 FAIL (Global Phantoms/API): {len(global_errors)}")
        for e in global_errors: print(f"  - {e}")
        
    if global_errors or active_errors:
        print(f"\n❌ Population Audit Failed: {len(global_errors)} Global, {len(active_errors)} Active Issues.")
        sys.exit(1)
    else:
        print("\n✅ Population Integrity Passed.")
        sys.exit(0)

if __name__ == "__main__":
    audit_population()
