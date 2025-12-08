import pytest

@pytest.mark.asyncio
async def test_archives_analytics_arbiter_boss_judge_smoke(client, db_session):
    """
    Smoke test: ensure Archives Analytics Arbiter boss QA returns a valid BossEvalResult.
    """
    import os
    os.environ["EVALFORGE_MOCK_GRADING"] = "1"

    from arcade_app.models import BossDefinition
    
    # Seed the boss
    boss_slug = "boss-archives-analytics-arbiter"
    boss_def = BossDefinition(
        id=boss_slug,
        name="Archives Analytics Arbiter",
        rubric=boss_slug,
        world_id="world-sql",
        track_id="archives-senior-analytics-architect",
        difficulty="legendary",
        max_hp=100
    )
    db_session.add(boss_def)
    await db_session.commit()

    payload = {
        "world_slug": "world-sql",
        "boss_id": "boss-archives-analytics-arbiter",
        "mode": "smoke",
        "submission_markdown": """# Analytics Architecture Blueprint – Archives Analytics Arbiter

## Domain & Requirements
We operate a subscription SaaS product with self-serve signups, trials, and upgrades.
Stakeholders rely on dashboards for MRR, churn, activation, and cohort analyses.
We need trustworthy numbers, fast dashboards, and safe evolution of schemas over time.

## Core Schemas & Grain
Facts:
- `f_subscriptions` at **subscription-id + day** grain:
  - captures active state, plan, price, and lifecycle events.
- `f_events` at **user-id + event-id** grain for product usage.
Dimensions:
- `d_customer`, `d_plan`, `d_date`, `d_region`.

Canonical:
- Dashboards must read from marts built on `f_subscriptions` and `f_events`, not raw tables.
- Metric definitions live with the mart (e.g., dbt models + yaml).

## Performance & Scaling
- Partition large facts (`f_subscriptions`, `f_events`) by event_date / billing_date.
- Cluster by customer_id / subscription_id for locality of access.
- Encourage time-bounded queries by design: dashboards default to windows (e.g., last 90 days).
- Periodic review of query plans; we add or adjust clustering/indices based on real workloads.

## Quality & Tests
- Tests:
  - uniqueness tests on primary keys and natural keys.
  - not_null tests on critical fields (amount, plan_id, customer_id).
  - referential tests to ensure all foreign keys point to existing dims.
  - row-count reasonableness checks vs previous days.
- Any failing test blocks deploys to production warehouse.
- Alerting notifies the owning team when tests fail; loads are marked as suspect until resolved.

## Lineage & Governance
- We maintain lineage from raw ingestion tables -> staging -> core models -> marts.
- Lineage is tracked in the transformation tool and documented in a simple catalog.
- Each core table has:
  - an owner team,
  - a description,
  - a list of metrics that depend on it.
- Metrics are defined centrally with clear formulas and owners.

## Incidents & Recovery
- When a dashboard is wrong or stale:
  - We check recent pipeline runs, test results, and schema changes.
  - We support re-running only the affected ranges (e.g., last N days) to control cost.
- Rollback:
  - Prefer to mark bad partitions/versioned tables as deprecated and point consumers to the corrected version.
- Communication:
  - Incident template includes: blast radius, affected metrics, ETA to fix, and whether consumers should pause decisions.

## Rollout & Adoption
- Phase 1: Introduce canonical marts and move dashboards over.
- Phase 2: Enforce tests in CI/CD and require ownership on core models.
- Phase 3: Establish incident runbooks and review a few postmortems to refine the process.

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
    assert result["boss_slug"] == "boss-archives-analytics-arbiter"
    assert result["rubric_id"] == "boss-archives-analytics-arbiter"

    # Score & integrity
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 8

    # Check criteria exist and have scores
    crit = {c["id"]: c for c in result.get("criteria", [])}

    for key in [
        "schema_and_grain",
        "performance_and_scaling",
        "quality_and_governance",
        "incidents_and_recovery"
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(result.get("strengths", []), list)
    assert isinstance(result.get("improvements", []), list)
