import pytest
import traceback
from arcade_app.models import BossDefinition

@pytest.mark.asyncio
async def test_sandbox_warden_boss_judge_smoke(client, patch_tracks_for_judge, judge_smoke_session, db_session, monkeypatch):
    """
    Smoke test: ensure Sandbox Warden boss QA path returns a valid BossEvalResult.
    This uses the ZERO boss judge sandbox prompt + rubric + golden runbook.
    """
    try:
        # SEED BOSS DEFINITION
        boss = BossDefinition(
            id="boss-grid-containment-sandbox-warden",
            name="Sandbox Warden",
            description="Infra boss",
            rubric="boss-grid-containment-sandbox-warden",
            base_xp_reward=500,
            max_hp=100,
            difficulty="hard",
            enabled=True
        )
        db_session.add(boss)
        await db_session.commit()

        # Enable Mock Grading Mode to bypass Vertex AI auth/mocks issues
        monkeypatch.setenv("EVALFORGE_MOCK_GRADING", "1")

        # The payload we send. API expects 'submission_markdown' which is passed to judge.
        # We add "MAGIC_BOSS_PASS" to ensure the mock judge awards full score (8/8).
        payload = {
            "world_slug": "world-infra",
            "boss_id": "boss-grid-containment-sandbox-warden",
            "mode": "smoke",
            "submission_markdown": """# Sandbox Warden Smoke Runbook

MAGIC_BOSS_PASS

## Incident Summary
Sandbox health check failing; investigating ports, disk, and services.
"""
        }
        
        # Send request
        resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
        
        if resp.status_code != 200:
            raise Exception(f"Status Code {resp.status_code}. Body: {resp.text}")

        data = resp.json()
        
        # The endpoint returns { results: [...], overall_pass: ... }
        if len(data["results"]) != 1:
            raise Exception(f"Expected 1 result, got {len(data['results'])}: {data}")
            
        res = data["results"][0]

        # Basic shape checks – match BossEvalResult contract
        if res["boss_slug"] != "boss-grid-containment-sandbox-warden":
             raise Exception(f"Slug mismatch: {res['boss_slug']}")
        
        # Mock grader with MAGIC_BOSS_PASS should return max score (8)
        if res["score"] != 8:
             raise Exception(f"Score mismatch: {res['score']} != 8. Result: {res}")
             
        if res["min_score_required"] != 6:
             raise Exception(f"Min Score mismatch: {res['min_score_required']}")
             
        if res["passed"] is not True:
             raise Exception(f"Passed mismatch: {res['passed']}")
    
    except Exception as e:
        with open("debug_failure.txt", "w") as f:
            f.write(f"TEST FAILED: {e}\n")
            f.write(traceback.format_exc())
        raise e
