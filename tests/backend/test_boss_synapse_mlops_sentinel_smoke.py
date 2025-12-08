import pytest

@pytest.mark.asyncio
async def test_synapse_mlops_sentinel_boss_judge_smoke(client, vertex_text):
    """
    Smoke test: ensure ML Ops Sentinel boss QA returns a valid BossEvalResult
    with scores, integrity, and feedback.
    """

    payload = {
        "world_slug": "world-ml",
        "boss_id": "boss-synapse-mlops-sentinel",
        "mode": "smoke",
        "submission_markdown": """# ML Platform Modernization Runbook – ML Ops Sentinel

## Context & Current Pain
We inherited scattered notebooks and scripts that train models directly against production-like tables.
Deployments are manual and undocumented, and monitoring is partial and inconsistent.

## Target Architecture – Data, Features, Models
- Introduce a feature store with versioned feature definitions and owners.
- Separate project-specific pipelines from shared platform services (feature store, model registry, artifact storage).
- Clearly define ownership for data ingestion, feature definitions, and model lifecycle.

## Training & CI/CD Pipeline
- Standardize training entrypoints that read configuration from versioned files.
- CI runs unit tests, data-contract checks, and training smoke tests on sampled data.
- CD promotes models through dev → staging → prod with evaluation gates and automatic metadata registration in the registry.

## Promotion, Canarying & Rollback
- Compare candidate vs current production model on held-out and prod-like evaluation sets.
- Use canary deployments with traffic splits and automated rollback on regressions or SLO violations.
- Provide a one-click rollback to the previous model version in the registry.

## Monitoring, Drift & Fairness
- Track latency, error rates, and key business KPIs per model and segment.
- Monitor data and target drift per key segment (e.g., region, device, risk bucket).
- Surface a minimal fairness view with performance deltas across allowed sensitive segments, with follow-up steps.

## Governance, Approvals & Auditability
- Require a model card and risk assessment for any model promoted to prod.
- Record approvals and deployment metadata (who, when, what changed) in an audit log.
- Retain artifacts and metadata long enough to support investigations and audits.

## Phased Rollout Plan
- Phase 1: standardize training entrypoints and artifact storage.
- Phase 2: introduce CI/CD with promotion gates and canaries on a pilot model.
- Phase 3: add monitoring, drift detection, and minimal fairness checks.
- Phase 4: formalize governance and expand platform to additional teams.
"""
    }

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    assert resp.status_code == 200

    report = resp.json()
    # Handle WorldBossQAReport wrapper
    # The API returns 'results': List[BossQAStatus]
    assert len(report["results"]) == 1
    data = report["results"][0]

    # Basic identity checks
    assert data["boss_slug"] == "boss-synapse-mlops-sentinel" # boss_id -> boss_slug in BossQAStatus
    # assert data["world_slug"] == "world-ml" # Removed: BossQAStatus doesn't have world_slug
    # assert data["track_id"] == "synapse-senior-mlops" # Removed: BossQAStatus doesn't have track_id
    assert data["rubric_id"] == "boss-synapse-mlops-sentinel"

    # Score + integrity
    assert isinstance(data["score"], int) # total_score -> score in BossQAStatus
    assert 0 <= data["score"] <= 8

    # BossQAStatus uses 'integrity_after'
    assert isinstance(data["integrity_after"], (int, float)) 
    assert 0.0 <= data["integrity_after"] <= 100.0

    assert isinstance(data["passed"], bool)
    assert isinstance(data["summary"], str)
    assert data["summary"].strip()

    # Criteria structure. BossQAStatus has 'criteria' list.
    crit = {c.get("id", c.get("key")): c for c in data.get("criteria", [])}

    for key in [
        "lifecycle_and_architecture",
        "ci_cd_and_promotion_strategy",
        "monitoring_drift_and_fairness",
        "governance_and_risk_controls",
    ]:
        assert key in crit
        # Check score (might be 'score' or 'band_score')
        item_score = crit[key].get("score")
        if item_score is None: item_score = crit[key].get("band_score")
        assert item_score in (0, 1, 2)
        
        assert isinstance(crit[key]["feedback"], str) # rubric field 'feedback' or 'rationale'? User prompt says "feedback".

    # Feedback lists
    assert isinstance(data.get("strengths", []), list)
    assert isinstance(data.get("improvements", []), list)
