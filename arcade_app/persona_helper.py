import json
import os
from functools import lru_cache
from typing import Dict, Any

# Path to the npcs.json file
NPCS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "npcs.json")

@lru_cache(maxsize=1)
def load_npcs() -> Dict[str, Dict[str, Any]]:
    """
    Loads NPC definitions from the JSON file.
    """
    if not os.path.exists(NPCS_PATH):
        return {}
    
    with open(NPCS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_npc(role: str) -> Dict[str, Any]:
    """
    Retrieves a specific NPC definition by role (e.g. 'quest', 'judge').
    Returns a generic fallback if not found.
    """
    npcs = load_npcs()
    if role in npcs:
        return npcs[role]
    
    # Fallback
    return {
        "id": "npc_system",
        "name": "SYSTEM",
        "title": "Generic Assistant",
        "color": "text-zinc-400",
        "avatar_icon": "cpu",
        "voice_prompt": "You are a helpful but neutral assistant.",
    }

def wrap_prompt_with_persona(base_prompt: str, role: str) -> str:
    """
    Wraps a base system prompt with the NPC's identity protocol.
    """
    npc = get_npc(role)
    return f"""
IDENTITY PROTOCOL:
{npc['voice_prompt']}

---
TASK:
{base_prompt}
""".strip()
