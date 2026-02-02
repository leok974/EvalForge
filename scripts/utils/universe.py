
import os
import json

def load_universe_map(root_dir):
    """Loads the big universe JSON to map slug -> metadata."""
    path = os.path.join(root_dir, "docs", "evalforge_world_content_remaining.json")
    if not os.path.exists(path):
        return {}
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"DEBUG: Failed to load {path}: {e}")
        return {}
        
    mapping = {}
    
    # The file structure can be { worlds: [...] } or just [...]
    if isinstance(data, dict):
        worlds = data.get("worlds", [])
    elif isinstance(data, list):
        worlds = data
    else:
        worlds = []

    for world in worlds:
        if "tracks" in world:
            for track in world["tracks"]:
                if "quests" in track:
                    for q in track["quests"]:
                        slug = q.get("quest_id") or q.get("slug")
                        if slug:
                            # Augment with track/world info if missing
                            if "track_id" not in q: q["track_id"] = track.get("track_id")
                            if "world_slug" not in q: q["world_slug"] = world.get("world_slug")
                            mapping[slug] = q
    return mapping

def get_starter_quests(root_dir):
    """Identifies starter quests (Order 1 in each track)."""
    mapping = load_universe_map(root_dir)
    starters = []
    
    # Organize by track
    tracks = {}
    for slug, q in mapping.items():
        tid = q.get("track_id", "unknown")
        if tid not in tracks: tracks[tid] = []
        tracks[tid].append(q)
        
    # Sort and pick first
    for tid, quests in tracks.items():
        # Sort by order_index, then slug
        quests.sort(key=lambda x: (x.get("order_index", 999), x.get("quest_id", "")))
        if quests:
            starter = quests[0]
            s_slug = starter.get("quest_id") or starter.get("slug")
            if s_slug:
                starters.append(s_slug)
                
    return starters
