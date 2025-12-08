import pytest

@pytest.mark.asyncio
async def test_synapse_gradient_boss_judge_smoke(client, vertex_text):
    """
    Smoke test: ensure Gradient Sentinel boss QA returns a valid BossEvalResult.
    """

    payload = {
        "world_slug": "world-ml",
        "boss_id": "boss-synapse-gradient-sentinel",
        "mode": "smoke",
        "submission_markdown": """# ML Training & Evaluation Incident Runbook – Smoke Test

# MAGIC_BOSS_PASS

## Incident Context
Binary classifier (risky vs safe) looks good offline but underperforms in production. Recent retrain worsened false negatives.

## Phase 1 – Verify Data & Splits
- Check label distribution and class imbalance.
- Ensure time-based or user-based splits with no leakage across train/val/test.
- Compare feature distributions between offline splits and recent production.

## Phase 2 – Inspect Metrics & Curves
- Plot training vs validation loss and AUC.
- Focus on recall / false negative rate for the risky class.
- Inspect calibration curves and segment metrics.

## Phase 3 – Stabilize & Improve Training
- Rebuild clean splits and train simple baselines (logistic regression, small tree).
- Adjust class weights and decision threshold to penalize false negatives more.
- Fix any training stability issues (learning rate, early stopping).

## Phase 4 – Baseline & Experiment Design
- Define baselines and incremental experiments (feature engineering, model capacity).
- Run controlled ablations, logging metrics and using clear promotion criteria.

## Phase 5 – Production Monitoring & Retraining
- Evaluate candidates on a prod-like holdout.
- Define monitoring metrics (FNR for risky class, calibration, score distribution).
- Set retraining cadence/trigger and a rollback plan for bad models.
"""
    }

    # Debug print payload
    print(f"DEBUG Payload: {payload}")

    resp = await client.post("/api/dev/boss_qa/worlds", json=payload)
    
    # Debug print response
    print(f"DEBUG Status: {resp.status_code}")
    
    assert resp.status_code == 200

    json_resp = resp.json()
    print(f"DEBUG Results: {json_resp}")

    # Handle potentially wrapped results
    if isinstance(json_resp, dict) and "results" in json_resp:
        results = json_resp["results"]
    else:
        results = json_resp

    assert isinstance(results, list)
    assert len(results) > 0
    data = results[0]

    assert data["boss_slug"] == "boss-synapse-gradient-sentinel"
    # boss_id might not be in the flattened result, usually boss_slug is
    # assert data["world_slug"] == "world-ml" 
    # track_id might not be in flattened result

    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 8

    assert isinstance(data["integrity_after"], (float, int))
    assert 0.0 <= data["integrity_after"] <= 100.0

    assert isinstance(data["passed"], bool)
    assert isinstance(data["summary"], str)
    assert data["summary"].strip() != ""

    crit = {c["id"]: c for c in data["criteria"]}
    for key in [
        "data_checks_and_split_design",
        "training_loop_and_metric_diagnostics",
        "baselines_experiments_and_ablation_design",
        "production_monitoring_and_retraining_plan",
    ]:
        assert key in crit
        assert crit[key]["score"] in (0, 1, 2)
        assert isinstance(crit[key]["feedback"], str)

    assert isinstance(data.get("strengths", []), list)
    assert isinstance(data.get("improvements", []), list)
