
import json
import os
from pathlib import Path
from typing import Set, Dict, List

# Cache the active set to avoid disk I/O on every request
_ACTIVE_SLUGS_CACHE: Set[str] = set()
_SLUG_TO_PACK_CACHE: Dict[str, str] = {}
_LAST_LOAD_HASH = None

def get_active_quest_config(root_dir: str = os.getcwd()) -> tuple[Set[str], Dict[str, str]]:
    """
    Returns (active_slugs, slug_to_pack_name_map).
    Parses configs/questpacks_active.json and all referenced packs.
    """
    global _ACTIVE_SLUGS_CACHE, _SLUG_TO_PACK_CACHE
    
    # Simple caching strategy: Just load it. 
    # For hot-reload dev, we might want to clear this or checking mtime, 
    # but for now, load-on-call is fine if files are small, or strict cache.
    # Let's do load-on-call for correctness during dev edits.
    
    # Robust root detection (relative to this file)
    # File: arcade_app/services/quest_visibility.py -> Root is 3 levels up
    file_path = Path(__file__).resolve()
    root = file_path.parents[2]
    
    # Fallback to provided root_dir if passed explicitly (e.g. tests)
    if root_dir != os.getcwd():
        root = Path(root_dir)

    config_path = root / "configs" / "questpacks_active.json"
    
    if not config_path.exists():
        print(f"❌ [QuestVisibility] Config NOT found at: {config_path}")
        return set(), {}
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except:
        return set(), {}

    active_slugs = set()
    slug_map = {}
    
    questpacks = config.get("active_questpacks", [])
    
    for pack_rel in questpacks:
        pack_path = root / pack_rel
        pack_name = pack_path.name 
        
        if not pack_path.exists():
            continue
            
        try:
            with open(pack_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            continue
            
        quests = []
        if isinstance(data, list): quests = data
        elif isinstance(data, dict):
            if "packs" in data: quests = data["packs"]
            elif "quests" in data: quests = data["quests"]
            elif "slug" in data: quests = [data]
            
        for q in quests:
            slug = q.get("slug")
            # Handle external
            if not slug and "quest_path" in q:
                q_dir = root / q["quest_path"]
                q_json = q_dir / "quest.json"
                if q_json.exists():
                    try:
                        with open(q_json, "r", encoding="utf-8") as qf:
                            slug = json.load(qf).get("slug")
                    except: pass
            
            if slug:
                # Check for explicit excluded visibility even in active pack?
                # User directive says "active_only" based on file inclusion.
                # But also check for "visibility": "internal" override inside the json?
                # "ensure internal/quarantined questpacks never surface... unless include_internal=1"
                
                # Check quest metadata for visibility: "internal"
                vis = q.get("visibility", "public")
                if vis == "internal":
                    # We might want to track these separately, but if the goal is 
                    # "active-only", and they are in the active file but marked internal,
                    # they should arguably be HIDDEN by default.
                    # But the CANARY requirement says we want to run them in CI.
                    # So maybe we exclude them from the "public_active_set" but include in "all_active_set"?
                    # Let's rely on the router to filter.
                    pass

                active_slugs.add(slug)
                slug_map[slug] = pack_name
                
    return active_slugs, slug_map
