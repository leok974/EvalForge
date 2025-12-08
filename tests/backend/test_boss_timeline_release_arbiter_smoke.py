import pytest

@pytest.mark.asyncio
async def test_timeline_release_arbiter_boss_judge_smoke(client, db_session):
    """
    Smoke test: ensure Timeline Release Arbiter boss QA returns a valid BossEvalResult.
    """
    import os
    os.environ["EVALFORGE_MOCK_GRADING"] = "1"

    from arcade_app.models import BossDefinition
    
    # Seed the boss
    boss_slug = "boss-timeline-release-arbiter"
    boss_def = BossDefinition(
        id=boss_slug,
        name="Timeline Release Arbiter",
        rubric=boss_slug,
        world_id="world-git",
        track_id="timeline-senior-release-architect",
        difficulty="legendary",
        max_hp=100
    )
    db_session.add(boss_def)
    await db_session.commit()

    payload = {
        "world_slug": "world-git",
        "boss_id": "boss-timeline-release-arbiter",
        "mode": "smoke",
        "submission_markdown": """# Release & History Blueprint – Timeline Release Arbiter

## Context & Product
We are a mid-sized team (12 engineers) shipping a web app plus background workers
from a single monorepo. We have dev, staging, and production environments and want
a predictable release cadence with safe hotfixes.

## Branching & Environments
- `main`: always releasable; protected; requires passing CI and reviews.
- `develop`: integration branch; used for feature work that is not production-ready.
- `release/x.y`: short-lived branches cut from `main` when we start stabilizing a minor release.
- `hotfix/x.y.z`: branches cut from the current production tag for urgent fixes.

Environment mapping:
- Dev: deploys from `develop` (or feature flags off `main` in phase 2).
- Staging: deploys from `release/x.y` during stabilization.
- Prod: deploys from annotated tags on `main`.

Branches have clear owners and deletion rules:
- `release/*` and `hotfix/*` are deleted after they are merged and tagged.

## Release Train & Cadence
- Two-week iterations on `develop`, merging ready work to `main` behind feature flags.
- When we decide to ship, we cut `release/x.y` from `main`, freeze new features,
  and only accept bugfix PRs that target the release branch.
- Once all checks and smoke tests pass on staging, we tag `vX.Y.0` on `main` and deploy to prod.
- Tagging script:
  - verifies commit is merged from `release/x.y`,
  - creates an annotated tag,
  - generates a basic changelog from merged PRs.

## Hotfix & Backport Flow
- Urgent fixes:
  - Cut `hotfix/x.y.z` from the latest production tag.
  - Apply the minimal fix, run CI, and deploy to staging then prod.
- Merge directions:
  - `hotfix/x.y.z` -> merge back into `main`.
  - If a `release/x.(y+1)` branch is open, also cherry-pick there when relevant.
- We maintain a short runbook that spells out exactly which branches must get the fix.

## History Policy (Rebase vs Merge)
- `main` is never rebased; only fast-forward or merge commits from protected branches.
- Individual developers are encouraged to use `git rebase` on local feature branches before opening PRs.
- `release/*` and `hotfix/*` branches avoid history rewrite after they are public.
- Reverts:
  - We prefer `git revert` for production issues so history stays auditable.

## Debugging with the Timeline
- All production deploys correspond to annotated tags with release notes.
- Commit messages reference tickets/issues where applicable.
- When an incident happens:
  - Use tags to narrow the window.
  - Use `git log` and `git bisect` between known-good and known-bad versions.
  - Combine with metrics/logs to confirm the culprit commit.
- New engineers are onboarded with a short guide on how to read the release history.

## Rollout & Adoption Plan
- Phase 1: enforce branch protections and tagging for prod.
- Phase 2: adopt the release branch model and stabilization window.
- Phase 3: introduce hotfix/backport runbook and teach the process to the team.
- Phase 4: refine conventions as we learn from a few incident postmortems.

"""
    }

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    assert resp.status_code == 200

    data = resp.json()

    data = resp.json()

    # Validate WorldBossQAReport structure
    assert "results" in data
    assert len(data["results"]) >= 1
    
    result = data["results"][0]
    
    assert result["boss_slug"] == "boss-timeline-release-arbiter"
    assert result["rubric_id"] == "boss-timeline-release-arbiter"
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 8
    
    crit = {c["id"]: c for c in result.get("criteria", [])}

    for key in [
        "architecture_and_branching",
        "workflow_and_automation",
        "risk_and_recovery",
        "collaboration_and_auditability"
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(result.get("strengths", []), list)
    assert isinstance(result.get("improvements", []), list)
