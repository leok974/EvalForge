import json
import os
from functools import lru_cache
from typing import Dict, Any, Optional

# Path to the worlds.json file
WORLDS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "worlds.json")

@lru_cache(maxsize=1)
def load_worlds() -> Dict[str, Dict[str, Any]]:
    """
    Loads world definitions from the JSON file and returns a dictionary keyed by world ID.
    Cached to avoid repeated file I/O.
    """
    if not os.path.exists(WORLDS_PATH):
        return {}

    with open(WORLDS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    by_id = {}
    for w in data:
        by_id[w["id"]] = w
    return by_id

def get_world(world_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific world definition by ID.
    Returns None if not found.
    """
    return load_worlds().get(world_id)
