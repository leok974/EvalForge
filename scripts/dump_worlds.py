
import json
import glob
import os

def main():
    worlds = {}
    print(f"Scanning data/questpacks/*.json...")
    
    for p in glob.glob("data/questpacks/*.json"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            print(f"Error reading {p}: {e}")
            continue
            
        # Handle different structures
        quests = []
        if isinstance(d, list):
            quests = d
        elif isinstance(d, dict):
            quests = d.get("quests") or d.get("items") or d.get("quest_definitions") or d.get("packs") or []
        
        for q in quests:
            if not isinstance(q, dict):
                continue
                
            w = q.get("world_id") or q.get("world") or q.get("worldId")
            s = q.get("slug") or q.get("id")
            
            if w and s:
                worlds.setdefault(w, []).append(s)

    print("\n--- World Summary ---")
    for w in sorted(worlds):
        slugs = worlds[w]
        print(f"World: {w} ({len(slugs)} quests)")
        # Print first few slugs
        for s in slugs[:5]:
            print(f"  - {s}")
        if len(slugs) > 5:
            print(f"  ... and {len(slugs)-5} more")
            
if __name__ == "__main__":
    main()
