
import pytest
from fastapi.testclient import TestClient
from arcade_app.main import app

client = TestClient(app)

def test_tools_explain_contract():
    payload = {
        "quest_slug": "test-quest",
        "stdout": "Hello world",
        "stderr": "",
        "failing_tests": [],
        "user_skill_level": "novice"
    }
    response = client.post("/api/tools/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "summary" in data
    assert "what_happened" in data
    assert "why_it_failed" in data
    assert "next_steps" in data
    assert "relevant_codex_refs" in data
    assert isinstance(data["next_steps"], list)
    assert isinstance(data["relevant_codex_refs"], list)

def test_tools_explain_with_stderr():
    payload = {
        "quest_slug": "test-quest",
        "stdout": "",
        "stderr": "IndexError: list index out of range",
    }
    response = client.post("/api/tools/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "Runtime Error Detected"
    assert "IndexError" in data["why_it_failed"]

def test_tools_debug_contract():
    payload = {
        "quest_slug": "test-quest",
        "stdout": "",
        "stderr": "NameError: name 'x' is not defined",
    }
    response = client.post("/api/tools/debug", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "summary" in data
    assert "likely_root_causes" in data
    assert "fix_plan" in data
    assert "patch_proposal" in data
    assert "Crash Analysis" in data["summary"]
