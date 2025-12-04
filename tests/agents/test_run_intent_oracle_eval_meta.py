# tests/agents/test_run_intent_oracle_eval_meta.py

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys

# Add scripts/agents to path so we can import the module
sys.path.append(str(Path(__file__).parents[2] / "scripts" / "agents"))

import run_intent_oracle_eval as module  # type: ignore


def test_run_intent_oracle_eval_enriches_with_meta(tmp_path, monkeypatch, capsys):
    # Create a dummy candidate planner file with plan_actions()
    candidate = tmp_path / "candidate_planner.py"
    candidate.write_text(
        "def plan_actions(goal, tools):\n"
        "    return []\n",
        encoding="utf-8",
    )

    # Fake env
    monkeypatch.setenv("EVALFORGE_BASE_URL", "http://example.com")
    monkeypatch.setenv("EVALFORGE_API_TOKEN", "token")

    # 1) Patch session.get to return different snapshots for before/after
    # The module uses a global 'session' object.
    
    calls = {"profile": 0, "boss": 0}

    def fake_get(url, **kwargs):
        # Mock response object
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json = json_data
                self.status_code = status_code
            
            def json(self):
                return self._json
            
            def raise_for_status(self):
                if self.status_code >= 400:
                    raise Exception(f"HTTP {self.status_code}")

        if "/api/profile/me" in url:
            calls["profile"] += 1
            # First call (before): 100, second call (after): 85
            return MockResponse({"profile": {"integrity": 100 if calls["profile"] == 1 else 85}})
        
        if "/api/boss/current" in url:
            calls["boss"] += 1
            # First call (before): 100, second call (after): 40
            return MockResponse({"encounter": {"hp": 100 if calls["boss"] == 1 else 40}})
        
        if "/api/auth/github/callback" in url:
             return MockResponse({}, status_code=307)

        return MockResponse({})

    # Patch session.get on the module's session object
    monkeypatch.setattr(module.session, "get", fake_get)
    
    # Patch session.post for boss actions
    def fake_post(url, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json = json_data
                self.status_code = status_code
            def json(self): return self._json
            def raise_for_status(self): pass

        if "/api/boss/accept" in url:
            return MockResponse({"encounter_id": 123})
        if "/api/boss/submit" in url:
             return MockResponse({
                "status": "win",
                "score": 0.9,
                "rubric": {}
             })
        return MockResponse({})

    monkeypatch.setattr(module.session, "post", fake_post)


    # 3) Call main() with our candidate path
    # We need to mock sys.argv
    monkeypatch.setattr(sys, "argv", ["run_intent_oracle_eval.py", str(candidate)])
    
    # Prevent sys.exit
    monkeypatch.setattr(sys, "exit", lambda x: None)

    # Run main
    module.main()

    captured = capsys.readouterr()
    out = captured.out.strip()
    assert out, "Expected JSON output on stdout"

    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {out}")
        raise

    assert data["boss_id"] == "intent_oracle"
    assert data["success"] is True
    assert data["score"] == 0.9

    # Check meta enrichment
    assert data["integrity_before"] == 100
    assert data["integrity_after"] == 85
    assert data["integrity_delta"] == 85 - 100 == -15

    assert data["boss_hp_before"] == 100
    assert data["boss_hp_after"] == 40
    assert data["boss_hp_delta"] == 40 - 100 == -60
