import pytest
from arcade_app.quest_helper import _inflate_key_terms, quest_to_dict
from arcade_app.models import QuestDefinition

def test_inflate_key_terms_strings():
    """Verify that legacy string terms are inflated into objects."""
    input_terms = [
        "glossary/python/variable",
        "glossary/python/function-def",
        "codex:simple-term"
    ]
    
    inflated = _inflate_key_terms(input_terms)
    
    assert len(inflated) == 3
    assert inflated[0] == {
        "id": "term-0",
        "term": "Variable",
        "codex_ref": "glossary/python/variable"
    }
    assert inflated[1] == {
        "id": "term-1",
        "term": "Function Def",
        "codex_ref": "glossary/python/function-def"
    }
    assert inflated[2] == {
        "id": "term-2",
        "term": "Simple Term",
        "codex_ref": "codex:simple-term"
    }

def test_inflate_key_terms_mixed():
    """Verify that mixed string and object terms are handled correctly."""
    input_terms = [
        "glossary/python/loop",
        {
            "id": "explicit-id",
            "term": "Explicit Term",
            "codex_ref": "codex:explicit"
        }
    ]
    
    inflated = _inflate_key_terms(input_terms)
    
    assert len(inflated) == 2
    assert inflated[0]["term"] == "Loop"
    assert inflated[1]["term"] == "Explicit Term"

def test_inflate_key_terms_empty():
    """Verify empty input returns empty list."""
    assert _inflate_key_terms([]) == []
    assert _inflate_key_terms(None) == [] # Should handle None if passed directly, though implementation expects list

def test_quest_to_dict_uses_inflation():
    """Integration test: ensure quest_to_dict calls inflation."""
    # Mock a quest definition with string terms
    quest = QuestDefinition(
        slug="test-quest",
        world_id="world-test",
        track_id="track-test",
        title="Test Quest",
        short_description="Short",
        detailed_description="Detailed",
        key_terms=["glossary/python/test"]
    )
    
    # We call quest_to_dict with no state
    result = quest_to_dict(quest, None)
    
    assert "key_terms" in result
    terms = result["key_terms"]
    assert len(terms) == 1
    assert isinstance(terms[0], dict)
    assert terms[0]["term"] == "Test"
    
    # Versioning Check
    assert "schema_version" in result
    assert result["schema_version"] == "v2"
