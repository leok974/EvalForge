import json
from pathlib import Path
from typing import Set

def get_all_quest_slugs() -> Set[str]:
    """
    Scan all questpacks in data/questpacks to find every referenced quest slug.
    Supports both legacy (root list) and modern (dict with 'quests' key) formats.
    """
    slugs = set()
    base_dir = Path("data/questpacks")
    
    if not base_dir.exists():
        return slugs
    
    # 1. Scan root JSON files (Legacy List Format)
    for f in base_dir.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            
            # Format: [{"quest_path": "docs/quests/slug"}, ...]
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "quest_path" in item:
                        path_str = item["quest_path"]
                        # Extract basename as slug
                        slug = Path(path_str).name
                        slug = Path(path_str).name
                        slugs.add(slug)
            
            # Also handle Modern Dict in Root
            elif isinstance(data, dict) and "quests" in data:
                 for q in data["quests"]:
                     if "slug" in q:
                         slugs.add(q["slug"])
        except Exception as e:
            print(f"⚠️ Error parsing {f}: {e}")

    # 2. Scan _modern JSON files (Modern Dict Format)
    modern_dir = base_dir / "_modern"
    if modern_dir.exists():
        for f in modern_dir.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                
                # Format: {"quests": [{"slug": "slug", ...}, ...]}
                if isinstance(data, dict) and "quests" in data:
                    for q in data["quests"]:
                        if "slug" in q:
                            slugs.add(q["slug"])
            except Exception as e:
                print(f"⚠️ Error parsing {f}: {e}")
                
    return slugs

if __name__ == "__main__":
    all_slugs = get_all_quest_slugs()
    print(f"Found {len(all_slugs)} unique quests.")
    for s in sorted(all_slugs):
        print(f"- {s}")
