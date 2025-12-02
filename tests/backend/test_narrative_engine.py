import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from arcade_app.worlds_helper import get_world
from arcade_app.quest_helper import build_quest_system_prompt
from arcade_app.explain_helper import build_explain_system_prompt

def test_build_quest_system_prompt_includes_world_alias():
    # 1. Verify World Data Exists
    world = get_world("world-python")
    assert world is not None
    alias = world["narrative_config"]["alias"]
    assert alias == "THE FOUNDRY"

    # 2. Build Prompt
    system = build_quest_system_prompt(
        base_task="Create a list of integers.",
        track_id="python-fundamentals",
        world_id="world-python",
    )

    # 3. Assert Narrative Elements
    assert alias in system
    assert "TASK" in system
    assert "Create a list of integers." in system
    assert "Line Architect" in system # Role

def test_explain_prompt_uses_analogy_prompt():
    world = get_world("world-python")
    analog = world["narrative_config"]["analogy_prompt"]
    assert "factory and mechanics metaphors" in analog

    system = build_explain_system_prompt(
        user_question="What is a list comprehension?",
        world_id="world-python",
        codex_entry=None,
    )

    assert analog in system
    assert "THE FOUNDRY" in system

def test_explain_prompt_with_codex_trumps_general():
    system = build_explain_system_prompt(
        user_question="How do I defeat the boss?",
        world_id="world-evalforge",
        codex_entry={
            "id": "boss-guide",
            "title": "Reactor Core Boss Guide",
            "summary": "Strategy for the Reactor Core boss.",
            "body_markdown": "Always fix the failing tests first.",
        },
    )

    assert "Reactor Core Boss Guide" in system
    assert "Always fix the failing tests first." in system
    # Should still include world alias
    assert "THE CONSTRUCT" in system

if __name__ == "__main__":
    try:
        test_build_quest_system_prompt_includes_world_alias()
        print("✅ test_build_quest_system_prompt_includes_world_alias passed")
        test_explain_prompt_uses_analogy_prompt()
        print("✅ test_explain_prompt_uses_analogy_prompt passed")
        test_explain_prompt_with_codex_trumps_general()
        print("✅ test_explain_prompt_with_codex_trumps_general passed")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
