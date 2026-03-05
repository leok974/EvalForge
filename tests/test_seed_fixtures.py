import pytest
from pathlib import Path

from scripts.seed_evalforge_universe import build_quest_workspace

def test_build_quest_workspace_retains_fixtures(tmp_path: Path):
    # Setup mock quest directory with fixtures and public tests
    quest_dir = tmp_path / "sql-t2-mock"
    quest_dir.mkdir()
    
    fixtures_dir = quest_dir / "fixtures"
    fixtures_dir.mkdir()
    (fixtures_dir / "schema.sql").write_text("CREATE TABLE mock (id INT);", encoding="utf-8")
    
    public_dir = quest_dir / "grading" / "public"
    public_dir.mkdir(parents=True)
    (public_dir / "test_task.py").write_text("def test_mock(): pass", encoding="utf-8")
    
    # 1. Initial State (simulating a fresh seed from quest.json)
    quest_data = {
        "slug": "sql-t2-mock",
        "language": "sql",
        "workspace": {"files": []}
    }
    
    ws1 = build_quest_workspace(quest_dir, quest_data)
    files1 = ws1["files"]
    paths1 = [f["path"] for f in files1]
    
    assert "fixtures/schema.sql" in paths1
    assert "test_task.py" in paths1
    
    # Ensure content is correct
    schema_file = next(f for f in files1 if f["path"] == "fixtures/schema.sql")
    assert "CREATE TABLE mock" in schema_file["content"]
    
    # 2. Simulate Upsert Idempotence
    # If the workspace was already built and we process it again, it should not duplicate files
    quest_data_with_built_ws = {
        "slug": "sql-t2-mock",
        "language": "sql",
        "workspace": ws1  # Passing the previously built workspace safely
    }
    
    ws2 = build_quest_workspace(quest_dir, quest_data_with_built_ws)
    files2 = ws2["files"]
    paths2 = [f["path"] for f in files2]
    
    assert "fixtures/schema.sql" in paths2
    assert "test_task.py" in paths2
    
    # Check for duplication (lengths should match exactly)
    assert len(paths1) == len(paths2)
