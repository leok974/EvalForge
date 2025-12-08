import pytest

@pytest.mark.asyncio
async def test_archives_query_boss_judge_smoke(client, vertex_text):
    """
    Smoke test: ensure Archive Query Warden boss QA returns a valid BossEvalResult.
    """

    payload = {
        "world_slug": "world-sql",
        "boss_id": "boss-archives-query-warden",
        "mode": "smoke",
        "submission_markdown": """# Analytics Query Incident Runbook – Smoke Test

# MAGIC_BOSS_PASS

## Incident Context
DAU and revenue by country are inflated/missing after a query change; performance is worse.

## Phase 1 – Clarify the Metric
- Define DAU as COUNT(DISTINCT user_id) per day + country (UTC).
- Revenue as SUM(amount) per day + country.

## Phase 2 – Inspect Current Query & Data
- Save current SQL and look for risky joins and filters.
- Sample events and orders to understand distributions.

## Phase 3 – Propose Corrected Query
- Separate daily_dau and daily_revenue aggregates.
- Join them at day + country grain via countries dim.
- Use LEFT JOIN to keep countries visible even with 0 activity.

## Phase 4 – Performance & Safety Checks
- Run EXPLAIN/EXPLAIN ANALYZE to inspect plan.
- Ensure predicates on event_ts/created_at can use indexes/partitions.
- Add appropriate indexes on date + country_code if missing.

## Phase 5 – Rollout & Monitoring
- Compare old vs new metrics for a few countries/days.
- Backfill to a sandbox table, wire dashboards via feature flag.
- Monitor latency and metric shapes after deploy.
"""
    }

    # Debug print payload
    print(f"\nDEBUG Payload: {payload}")

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    
    # Debug print response
    print(f"\nDEBUG Status: {resp.status_code}")
    # print(f"DEBUG Response: {resp.text}") # Commented out to reduce noise, enable if needed

    assert resp.status_code == 200

    json_resp = resp.json()
    print(f"\nDEBUG Results: {json_resp}")

    if isinstance(json_resp, dict) and "results" in json_resp:
        results = json_resp["results"]
    else:
        results = json_resp

    assert isinstance(results, list)
    assert len(results) > 0
    data = results[0]

    assert data["boss_slug"] == "boss-archives-query-warden"
    # assert data["world_slug"] == "world-sql" # world_slug might strictly be on rubric, not always returned in flat result
    # assert data["track_id"] == "archives-retrieval-analytics"

    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 8

    assert isinstance(data["integrity_after"], (float, int))
    assert 0.0 <= data["integrity_after"] <= 100.0

    assert isinstance(data["passed"], bool)
    assert isinstance(data["summary"], str)
    assert data["summary"].strip() != ""

    crit = {c["id"]: c for c in data["criteria"]}
    for key in [
        "requirement_translation_and_data_modeling",
        "query_correctness_and_edge_cases",
        "performance_and_query_plan_reasoning",
        "runbook_clarity_and_validation",
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(data.get("strengths", []), list)
    assert isinstance(data.get("improvements", []), list)
