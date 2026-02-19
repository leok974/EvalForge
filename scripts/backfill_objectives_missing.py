
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from scripts.utils_questpacks import get_all_quest_slugs

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def backfill_missing_objectives(target_slug=None):
    print("🔧 Backfilling Missing Objectives...")
    
    # 1. Map slugs to sources
    slug_map = {} # slug -> {type: 'file'|'pack', path: Path, data: dict (if file) or index (if pack)}
    
    # Scan docs/quests
    for p in Path("docs/quests").rglob("quest.json"):
        try:
            data = load_json(p)
            if "slug" in data:
                slug_map[data["slug"]] = {"type": "file", "path": p}
        except:
            pass
            
    # Scan Questpacks
    pack_map = {} # path -> data
    for p in Path("data/questpacks").glob("*.json"):
        try:
            data = load_json(p)
            if "quests" in data:
                pack_map[p] = data
                for i, q in enumerate(data["quests"]):
                    if "slug" in q:
                        if q["slug"] not in slug_map: # Prefer file if exists
                            slug_map[q["slug"]] = {"type": "pack", "path": p, "index": i}
        except:
            pass

    targets = [target_slug] if target_slug else list(slug_map.keys())
    
    updated_count = 0
    
    for slug in targets:
        if slug not in slug_map:
            if target_slug: print(f"❌ Slug {slug} not found.")
            continue
            
        info = slug_map[slug]
        
        # Determine World/Strategy
        world = "unknown"
        if "node" in slug: world = "Node"
        elif "cli" in slug: world = "CLI"
        elif "html" in slug: world = "HTML"
        elif "css" in slug: world = "CSS"
        elif "react" in slug: world = "React"
        elif "sql" in slug: world = "SQL"
        elif "infra" in slug: world = "Infra"
        
        # Generate Objectives based on World
        new_objs = []
        if world in ["Node", "CLI", "React"]:
             new_objs = [
                 {
                     "id": "test_pass",
                     "kind": "tests_pass",
                     "text": "Correct solution implemented",
                     "why": "Functional requirement",
                     "rule": {
                         "must_pass": True
                     }
                 }
             ]
        elif world in ["HTML", "CSS"]:
             # Default to fs_snapshot of index.html/styles.css?
             # We can't know files easily without checking.
             # Placeholder: fs_snapshot ANY file?
             # Or source_regex ".*"
             new_objs = [
                 {
                     "id": "fs_check",
                     "kind": "fs_snapshot",
                     "text": "Required files exist",
                     "why": "Structure requirement",
                     "rule": {
                         "must_exist": ["index.html" if world=="HTML" else "styles.css"]
                     }
                 }
             ]
        elif world == "SQL":
             new_objs = [
                 {
                     "id": "sql_check",
                     "kind": "tests_pass", # Assuming SQL runner uses tests? Or sql_query_exact? 
                     # SQL usually uses sql_query_exact or tests_pass.
                     # Let's use tests_pass safe default if runner exists.
                     "text": "Query produces correct results",
                     "why": "Functional requirement",
                     "rule": {"must_pass": True}
                 }
             ]
        else:
             # Default fallback
             new_objs = [
                 {
                     "id": "default_pass",
                     "kind": "tests_pass", 
                     "text": "Tests pass",
                     "why": "Requirement",
                     "rule": {"must_pass": True}
                 }
             ]
        
        # Apply Update
        if info["type"] == "file":
             data = load_json(info["path"])
             # Only update if missing or legacy
             current = data.get("objectives", [])
             needs_update = False
             if not current:
                 needs_update = True
             else:
                 # Check for legacy (obj_default) OR missing kind/rule
                 for o in current:
                     if o.get("id") == "obj_default" or not o.get("kind") or not o.get("rule"):
                         needs_update = True
                         break
             
             if needs_update:
                 data["objectives"] = new_objs
                 save_json(info["path"], data)
                 print(f"✅ Updated {slug} in {info['path']}")
                 updated_count += 1
                 
        elif info["type"] == "pack":
             p_data = load_json(info["path"])
             q = p_data["quests"][info["index"]]
             
             current = q.get("objectives", [])
             needs_update = False
             if not current:
                 needs_update = True
             else:
                 for o in current:
                     if o.get("id") == "obj_default" or not o.get("kind") or not o.get("rule"):
                         needs_update = True
                         break
             
             if needs_update:
                 q["objectives"] = new_objs
                 save_json(info["path"], p_data)
                 print(f"✅ Updated {slug} in {info['path']}")
                 updated_count += 1

    print(f"✨ Backfilled {updated_count} quests.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Specific slug")
    args = parser.parse_args()
    backfill_missing_objectives(args.slug)
