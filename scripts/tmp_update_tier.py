import json
import os

PATHS = [
    "data/questpacks/python_systems.json",
    "data/questpacks/foundry_python.json"
]

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = False
    if isinstance(data, list):
        for q in data:
            if "tier" not in q or q["tier"] != 1:
                q["tier"] = 1
                updated = True
            # Also remove inline md to force file usage if possible, 
            # but let's just set tier first.
            # actually, let's remove inline briefing/lore to be clean
            if "briefing_md" in q:
                del q["briefing_md"]
                updated = True
            if "lore_md" in q:
                del q["lore_md"]
                updated = True

    if updated:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Updated {path}")
    else:
        print(f"No changes for {path}")

if __name__ == "__main__":
    for p in PATHS:
        if os.path.exists(p):
            update_file(p)
