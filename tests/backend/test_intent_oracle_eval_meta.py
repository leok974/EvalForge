# tests/backend/test_intent_oracle_eval_meta.py

from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from arcade_app.agent import app
from arcade_app.config import settings


client = TestClient(app)


def _make_subprocess_result(stdout: str, returncode: int = 0):
    m = MagicMock()
    m.stdout = stdout
    m.stderr = ""
    m.returncode = returncode
    return m


@patch("arcade_app.routers.intent_oracle_eval.subprocess.run")
def test_intent_oracle_eval_fallback_meta_fields(subprocess_run_mock):
    """
    When Antigravity is NOT configured, the endpoint should:
      - call the local eval script via subprocess
      - map integrity_* and boss_hp_* fields from the CLI JSON
    """
    # Ensure Antigravity is disabled
    # We need to mock settings properly. Since we are importing settings from config,
    # we should patch it where it is used or modify the object if it's a singleton.
    # The user's code modifies settings directly. Assuming settings is a Pydantic BaseSettings instance.
    
    # Ideally we use a fixture or patch.dict, but let's try direct modification as requested
    # and restore it after (or rely on test isolation if available, but explicit is better).
    
    # Let's use patch for safety
    with patch("arcade_app.routers.intent_oracle_eval.settings") as mock_settings:
        mock_settings.antigravity_base_url = None
        mock_settings.antigravity_api_token = None
        mock_settings.public_base_url = "http://localhost:8081"
        mock_settings.intent_oracle_eval_token = "mock-token"
        mock_settings.environment = "dev"

        # Minimal CLI JSON with meta fields
        cli_payload = {
            "boss_id": "intent_oracle",
            "success": True,
            "score": 0.9,
            "integrity_before": 100,
            "integrity_after": 90,
            "integrity_delta": -10,
            "boss_hp_before": 100,
            "boss_hp_after": 20,
            "boss_hp_delta": -80,
        }
        subprocess_run_mock.return_value = _make_subprocess_result(
            stdout=json.dumps(cli_payload)
        )

        resp = client.post("/api/agents/intent-oracle/eval", json={})
        assert resp.status_code == 200, resp.text

        data = resp.json()
        assert data["boss_id"] == "intent_oracle"
        assert data["success"] is True
        assert data["score"] == 0.9

        # Meta fields should be passed through unchanged
        assert data["integrity_before"] == 100
        assert data["integrity_after"] == 90
        assert data["integrity_delta"] == -10
        assert data["boss_hp_before"] == 100
        assert data["boss_hp_after"] == 20
        assert data["boss_hp_delta"] == -80

        # And we did call subprocess
        assert subprocess_run_mock.called


@patch("arcade_app.routers.intent_oracle_eval.httpx.post")
def test_intent_oracle_eval_antigravity_meta_fields(httpx_post_mock):
    """
    When Antigravity IS configured, the endpoint should:
      - call the Antigravity /api/subagents/run endpoint
      - map integrity_* and boss_hp_* fields from job['output']
    """
    with patch("arcade_app.routers.intent_oracle_eval.settings") as mock_settings:
        mock_settings.antigravity_base_url = "http://antigravity:8080"
        mock_settings.antigravity_api_token = "dummy-token"
        mock_settings.public_base_url = "http://localhost:8081"
        mock_settings.intent_oracle_eval_token = "mock-token"

        job_payload = {
            "status": "completed",
            "output": {
                "boss_id": "intent_oracle",
                "success": False,
                "score": 0.42,
                "integrity_before": 90,
                "integrity_after": 60,
                "integrity_delta": -30,
                "boss_hp_before": 80,
                "boss_hp_after": 60,
                "boss_hp_delta": -20,
            },
        }

        httpx_post_mock.return_value = MagicMock(
            status_code=200,
            json=lambda: job_payload,
            text=json.dumps(job_payload),
        )

        resp = client.post("/api/agents/intent-oracle/eval", json={})
        assert resp.status_code == 200, resp.text

        data = resp.json()
        assert data["success"] is False
        assert data["score"] == 0.42

        assert data["integrity_before"] == 90
        assert data["integrity_after"] == 60
        assert data["integrity_delta"] == -30
        assert data["boss_hp_before"] == 80
        assert data["boss_hp_after"] == 60
        assert data["boss_hp_delta"] == -20

        assert httpx_post_mock.called
