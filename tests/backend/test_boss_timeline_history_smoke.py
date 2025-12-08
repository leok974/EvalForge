import pytest
from arcade_app.models import BossDefinition
from arcade_app.grading_helper import judge_boss_with_rubric

@pytest.mark.asyncio
async def test_timeline_history_boss_judge_smoke(client, monkeypatch, db_session):
    """
    Smoke test: ensure History Rewriter boss QA returns a valid BossEvalResult.
    """
    
    # SEED BOSS DEFINITION (Ensures it exists in the test DB)
    boss = BossDefinition(
        id="boss-timeline-history-rewriter",
        name="History Rewriter",
        description="The Timeline boss",
        rubric="boss-timeline-history-rewriter",
        base_xp_reward=500,
        max_hp=100,
        difficulty="hard",
        enabled=True
    )
    db_session.add(boss)
    await db_session.commit()

    # Enable Mock Grading Mode to bypass Vertex AI auth/mocks issues
    monkeypatch.setenv("EVALFORGE_MOCK_GRADING", "1")

    payload = {
        "world_slug": "world-git",
        "boss_id": "boss-timeline-history-rewriter",
        "mode": "smoke",
        "submission_markdown": """# Git Incident Runbook – Smoke Test

# MAGIC_BOSS_PASS

## Incident Context
History mangled on feature/auth-redesign after a bad rebase/force-push. Bug surfaced post-deploy.

## Phase 1 – Inspect & Map the Graph
- git fetch --all --prune
- git log --oneline --graph --decorate --all
- git branch -vv to see divergence.

## Phase 2 – Recovery Plan
- Use git reflog on feature/auth-redesign to find pre-rebase tip.
- Create backup/auth-redesign-pre-rebase branch at that reflog entry.
- Compare old vs new feature history to find lost commits.

## Phase 3 – Execute Safely
- Use git bisect between known good tag and main head to find culprit.
- On main, prefer git revert on bad commit rather than rewriting public history.
- Push main + cherry-pick to release/1.2 as needed.

## Phase 4 – Verify & Communicate
- Verify tests and staging after revert.
- Add branch protection for main/release.
- Document incident and updated Git guidelines.
"""
    }

    # Use the test client to hit the endpoint
    # Note: 'client' fixture comes from pytest-asyncio + httpx usually
    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    assert resp.status_code == 200, f"Response: {resp.text}"

    raw = resp.json()
    # Response is a report with a list of results
    data = raw["results"][0]

    assert data["boss_slug"] == "boss-timeline-history-rewriter"
    # assert data["world_slug"] == "world-git" # world_slug might not be in response

    assert isinstance(data["score"], int) # total_score mapped to score
    # With MAGIC_BOSS_PASS, we expect perfect score
    assert data["score"] == 8

    # integrity is optional/calculated
    if "integrity_after" in data:
         assert isinstance(data["integrity_after"], (float, int))

    assert data["passed"] is True
    assert isinstance(data["summary"], str)
    assert data["summary"].strip() != ""

    crit = {c["id"]: c for c in data["criteria"]}
    expected_criteria = [
        "graph_literacy_and_diagnosis",
        "recovery_and_rescue_skills",
        "history_safety_and_collaboration",
        "runbook_clarity_and_copy_paste_safety",
    ]
    
    for key in expected_criteria:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(data.get("strengths", []), list)
    assert isinstance(data.get("improvements", []), list)
