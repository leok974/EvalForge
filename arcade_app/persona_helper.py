import json
import os
from typing import Dict, Any

_NPC_CACHE = None

def get_npc(role: str) -> Dict[str, Any]:
    """
    Loads the NPC config for a given role (quest, judge, etc).
    """
    global _NPC_CACHE
    if not _NPC_CACHE:
        try:
            with open("data/npcs.json", "r") as f:
                _NPC_CACHE = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load NPCs: {e}")
            _NPC_CACHE = {}
    
    # Return specific NPC or a generic fallback
    return _NPC_CACHE.get(role, {
        "id": "npc_system",
        "name": "SYSTEM",
        "title": "Core Process",
        "color": "zinc",
        "avatar_icon": "cpu",
        "voice_prompt": "You are a helpful assistant."
    })

def wrap_prompt_with_persona(base_prompt: str, role: str) -> str:
    """
    Injects the personality into the system prompt.
    Respects global override flag for 'Serious Mode'.
    """
    if os.getenv("EVALFORGE_PERSONAS", "full") == "off":
        return base_prompt

    npc = get_npc(role)
    
    return f"""
    IDENTITY PROTOCOL:
    {npc['voice_prompt']}
    
    ---
    TASK:
    {base_prompt}
    """
