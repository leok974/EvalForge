import pytest

@pytest.mark.asyncio
async def test_grid_resilience_warden_boss_judge_smoke(client, db_session):
    """
    Smoke test: ensure Grid Resilience Warden boss QA returns a valid BossEvalResult.
    """
    import os
    os.environ["EVALFORGE_MOCK_GRADING"] = "1"

    from arcade_app.models import BossDefinition
    
    # Seed the boss
    boss_slug = "boss-grid-resilience-warden"
    boss_def = BossDefinition(
        id=boss_slug,
        name="Grid Resilience Warden",
        rubric=boss_slug,
        world_id="world-infra",
        track_id="grid-senior-sre-architect",
        difficulty="legendary",
        max_hp=100
    )
    db_session.add(boss_def)
    await db_session.commit()

    payload = {
        "world_slug": "world-infra",
        "boss_id": "boss-grid-resilience-warden",
        "mode": "smoke",
        "submission_markdown": """# Resilience Architecture Blueprint – Grid Resilience Warden

## System Context & SLOs
Global e-commerce service. 
SLO: 99.95% Availability (monthly).
SLI: Successful requests / Total requests (measured at LB).
Failure Domains: 3 Regions, 3 AZs per region.

## Failure Architecture & Mitigations
- Circuit Breakers: Client-side breakers on all inter-service calls.
- Timeouts: Strict aggressive timeouts (P99 + buffer).
- Isolation: Cellular architecture (sharding by customer ID range) to limit blast radius.
- Load Shedding: API Gateway drops low-priority traffic when saturation > 85%.

## Observability & Alerting
- Signals: RED metrics (Rate, Errors, Duration) for all services.
- Logging: Structured JSON logs with trace IDs.
- Alerting: Burn-rate based alerting on error budget consumption (e.g. page if 2% of budget burns in 1 hour).

## Deployment & Safety
- Pipeline: CI -> Staging (Integration) -> Canary (1%) -> Production (Zone by Zone).
- Automated Rollback: Triggered if error rate > threshold during rollout.
- Config Safety: Config schema validation + segregated rollout from code.

## Incident Management & Learning
- Roles: Incident Commander (IC) leads, Ops Scribe logs events.
- Mitigate First: Focus on restoring service (rollback, shed load) before debugging root cause.
- Postmortem: Blameless RCA within 48h. Action items prioritized in backlog. Game Days held quarterly to test assumptions.

"""
    }

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    assert resp.status_code == 200

    data = resp.json()

    # Validate structure
    assert "results" in data
    assert len(data["results"]) >= 1
    
    result = data["results"][0]

    # Identity checks
    assert result["boss_slug"] == "boss-grid-resilience-warden"
    assert result["rubric_id"] == "boss-grid-resilience-warden"

    # Score & integrity
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 8

    # Check criteria exist and have scores
    crit = {c["id"]: c for c in result.get("criteria", [])}

    for key in [
        "slo_and_error_budgets",
        "failure_mitigation",
        "observability_and_alerts",
        "incident_lifecycle"
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(result.get("strengths", []), list)
    assert isinstance(result.get("improvements", []), list)
