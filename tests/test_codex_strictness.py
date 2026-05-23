import os
import glob
import json
from pathlib import Path
import pytest

def test_no_data_codex_remains():
    """Ensure data/codex contains no markdown files definitively."""
    data_codex_path = Path("data/codex")
    if data_codex_path.exists():
        md_files = list(data_codex_path.rglob("*.md"))
        assert len(md_files) == 0, f"Found deprecated files in data/codex: {md_files}"

def test_no_duplicate_codex_slugs():
    """Ensure no two codex files share the same filename in docs/codex/"""
    codex_root = Path("docs/codex")
    if not codex_root.exists():
        pytest.skip("docs/codex does not exist locally")
        
    seen = {}
    duplicates = []
    
    for md_file in codex_root.rglob("*.md"):
        filename = md_file.name
        if filename in ("README.md", "README-docs.md", "index.md", "systems.md", "memory.md"):
            continue
            
        if filename in seen:
            duplicates.append(f"{filename} found at {md_file} and {seen[filename]}")
        else:
            seen[filename] = md_file
            
    assert len(duplicates) == 0, f"Duplicate codex slugs found:\\n" + "\\n".join(duplicates)

def test_boss_indexes_use_docs_codex():
    """Ensure all boss codex indexes reference docs/codex/"""
    boss_indexes = Path("docs").glob("boss_codex_index.*.json")
    for idx_file in boss_indexes:
        with open(idx_file, "r") as f:
            data = json.load(f)
            # data is usually a dict tracking boss codex entries
            raw_content = json.dumps(data)
            assert "data/codex" not in raw_content, f"Deprecated data/codex found in {idx_file}"
            
def test_no_legacy_quest_metadata():
    """Scan all active quest JSONs ensuring none use legacy aliases."""
    import sys
    sys.path.append(os.path.abspath("."))
    
    from scripts.questpack_seed import find_json_files
    files = find_json_files(os.getcwd())
    
    legacy_keys = {"world_slug", "track_slug", "hints"}
    violations = []
    
    for f in files:
        if "questpacks" not in f and "quests" not in f:
             continue
             
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception:
            continue
            
        quests = []
        if isinstance(data, list):
            quests = data
        elif isinstance(data, dict):
            if "packs" in data:
                quests.extend(data["packs"])
            elif "quests" in data:
                quests.extend(data["quests"])
            elif "slug" in data or "id" in data:
                quests.append(data)
                
        for q in quests:
            for k in legacy_keys:
                if k in q:
                    violations.append(f"{q.get('slug')} uses legacy key '{k}'")
                    
    # Only fail if they are in core SQL tiers (for this migration wave specifically)
    # Actually, fail universally to be strict as requested.
    assert len(violations) == 0, f"Legacy metadata aliases found:\\n" + "\\n".join(violations)
