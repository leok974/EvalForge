from fastapi.testclient import TestClient
import os
import pytest
from unittest.mock import patch, MagicMock
from arcade_app.agent import app

client = TestClient(app)

@pytest.fixture
def mock_auth_env(monkeypatch):
    monkeypatch.setenv("EVALFORGE_AUTH_MODE", "mock")
    monkeypatch.setenv("EVALFORGE_MOCK_GRADING", "1")
    monkeypatch.setenv("EVALFORGE_API_TOKEN", "mock-token")
    # Mock Antigravity config
    monkeypatch.setenv("EVALFORGE_ANTIGRAVITY_BASE_URL", "http://mock-ag")
    monkeypatch.setenv("EVALFORGE_ANTIGRAVITY_API_TOKEN", "mock-ag-token")
    monkeypatch.setenv("EVALFORGE_INTENT_ORACLE_EVAL_TOKEN", "mock-eval-token")

def test_intent_oracle_eval_endpoint_fallback(mock_auth_env, tmp_path):
    # Create a tiny candidate_planner.py
    candidate = tmp_path / "candidate_planner.py"
    candidate.write_text("def plan(): pass", encoding="utf-8")

    # Override auth
    from arcade_app.auth_helper import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"id": "test-user", "name": "Test User"}

    # Mock settings to DISABLE Antigravity and force fallback
    with patch("arcade_app.routers.intent_oracle_eval.settings") as mock_settings:
        mock_settings.antigravity_base_url = None
        mock_settings.antigravity_api_token = None
        mock_settings.public_base_url = "http://localhost:8081"
        mock_settings.intent_oracle_eval_token = "mock-eval-token"
        mock_settings.environment = "dev"

        # Mock subprocess.run
        with patch("subprocess.run") as mock_subprocess:
            mock_subprocess.return_value.returncode = 0
            mock_subprocess.return_value.stdout = '{"boss_id": "intent_oracle", "success": true, "score": 0.88, "raw": {"rubric": {}}}'
            mock_subprocess.return_value.stderr = ""

            try:
                response = client.post(
                    "/api/agents/intent-oracle/eval",
                    json={"candidate_path": str(candidate)},
                )

                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert data["score"] == 0.88
                
                # Verify subprocess was called
                mock_subprocess.assert_called_once()

            finally:
                app.dependency_overrides = {}
