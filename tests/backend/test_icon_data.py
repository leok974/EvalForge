import pytest
import json
import os

def test_worlds_have_valid_icons():
    """
    Verify that every world in worlds.json has a valid 'icon' field
    that corresponds to a known Lucide icon name (string).
    """
    path = "data/worlds.json"
    assert os.path.exists(path), "worlds.json missing!"
    
    with open(path, "r", encoding="utf-8") as f:
        worlds = json.load(f)
        
    for w in worlds:
        assert "icon" in w, f"World {w['id']} is missing 'icon' field"
        assert isinstance(w["icon"], str), f"World {w['id']} icon must be a string"
        assert len(w["icon"]) > 0, f"World {w['id']} icon cannot be empty"
