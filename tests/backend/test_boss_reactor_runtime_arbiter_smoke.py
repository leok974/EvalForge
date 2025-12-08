import pytest

@pytest.mark.asyncio
async def test_reactor_runtime_arbiter_boss_judge_smoke(client, db_session):
    """
    Smoke test: ensure Reactor Runtime Arbiter boss QA returns a valid BossEvalResult.
    """
    import os
    os.environ["EVALFORGE_MOCK_GRADING"] = "1"

    from arcade_app.models import BossDefinition
    
    # Seed the boss
    boss_slug = "boss-reactor-runtime-arbiter"
    boss_def = BossDefinition(
        id=boss_slug,
        name="Reactor Runtime Arbiter",
        rubric=boss_slug,
        world_id="world-java",
        track_id="reactor-senior-runtime-architect",
        difficulty="legendary",
        max_hp=100
    )
    db_session.add(boss_def)
    await db_session.commit()

    payload = {
        "world_slug": "world-java",
        "boss_id": "boss-reactor-runtime-arbiter",
        "mode": "smoke",
        "submission_markdown": """# Reactor Architecture Blueprint – Reactor Runtime Arbiter

## Architecture & Boundaries
- Modular Monolith graduating to Services:
  - Core domain logic in `reactor-core` jar, agnostic of framework.
  - HTTP adapters in `reactor-api` module.
  - Workers in `reactor-worker`.
- Strict boundaries: No cyclic dependencies (enforced by ArchUnit).
- Contracts: Open API specs defined first; servers generated from spec.

## Runtime & JVM Performance
- Tuning based on workload:
  - High throughput API: G1GC with -XX:MaxGCPauseMillis=200.
  - Batch workers: ParallelGC for max throughput.
- Signals:
  - Enabled GC logs (-Xlog:gc*).
  - JFR enabled for on-demand profiling (5 min circular buffer).
- Sizing:
  - Heap set to 70% of container memory; awareness of container constraints (-XX:+UseContainerSupport).

## Concurrency & Resilience
- Thread Pools:
  - Bounded queues everywhere.
  - Separate thread pools for CPU-bound (processing) vs blocking I/O (DB calls).
- Resilience:
  - Resilience4j circuit breakers on all downstream service calls.
  - Retries only on idempotent operations (GETs), with exponential backoff.
  - Bulkheads to prevent one slow upstream from exhausting all threads.

## API Contracts & Evolution
- Versioning strategy: URL path (`/v1`, `/v2`) for breaking changes.
- Additive changes preferred.
- Deprecation policy: 6 months notice, `Deprecation` header sent to clients.

## Operability & Incident Handling
- Observability:
  - Metrics (Micrometer) for thread pool saturation, GC time, request rate/error/duration.
  - Structured Logging (JSON) with Correlation IDs injected via MDC.
- Incident Response:
  - Runbooks for "High Latency", "Queue Backup", "OOM".
  - Blameless Postmortems focused on process/tooling improvements, not human error.
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
    assert result["boss_slug"] == "boss-reactor-runtime-arbiter"
    assert result["rubric_id"] == "boss-reactor-runtime-arbiter"

    # Score & integrity
    assert isinstance(result["score"], int)
    assert 0 <= result["score"] <= 8

    # Check criteria exist and have scores
    crit = {c["id"]: c for c in result.get("criteria", [])}

    for key in [
        "architecture_boundaries",
        "runtime_performance",
        "concurrency_resilience",
        "api_evolution_operability"
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(result.get("strengths", []), list)
    assert isinstance(result.get("improvements", []), list)
