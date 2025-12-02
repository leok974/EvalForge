import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from arcade_app.persona_helper import get_npc, wrap_prompt_with_persona

def test_get_npc_known_role():
    kai = get_npc("quest")
    assert kai["name"] == "KAI"
    assert "Mission Control" in kai["title"]

def test_get_npc_unknown_role_falls_back():
    sys_npc = get_npc("unknown-role")
    assert sys_npc["name"] == "SYSTEM"

def test_wrap_prompt_includes_voice_prompt():
    base = "Explain recursion."
    wrapped = wrap_prompt_with_persona(base, "explain")
    assert "IDENTITY PROTOCOL:" in wrapped
    assert "Explain recursion." in wrapped
    assert "Archivist" in wrapped or "repository of knowledge" in wrapped

if __name__ == "__main__":
    try:
        test_get_npc_known_role()
        print("✅ test_get_npc_known_role passed")
        test_get_npc_unknown_role_falls_back()
        print("✅ test_get_npc_unknown_role_falls_back passed")
        test_wrap_prompt_includes_voice_prompt()
        print("✅ test_wrap_prompt_includes_voice_prompt passed")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
