#!/usr/bin/env python
"""
Example script demonstrating ZERO boss judge for ApplyLens bosses.
Shows how to construct submission_context for different boss types.

Usage:
    python scripts/example_zero_boss_judge.py
"""
import os
import sys
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def example_inbox_maelstrom():
    """Example: Judge the Inbox Maelstrom (runtime boss) submission."""
    from arcade_app.boss_rubric_helper import load_boss_rubric, score_boss_eval
    from arcade_app.boss_rubric_models import BossEvalLLMChoice
    from arcade_app.llm import call_zero_boss_judge
    
    print("=" * 60)
    print("EXAMPLE: Inbox Maelstrom (Runtime Boss)")
    print("=" * 60)
    
    # Load the rubric
    rubric = load_boss_rubric("applylens_runtime_boss")
    print(f"\nRubric: {rubric.title}")
    print(f"Dimensions: {len(rubric.dimensions)}")
    print(f"Max Score: {rubric.max_score}")
    
    # Construct submission context
    submission_context = {
        "summary": "Gmail ingest worker hardened with timeouts, retries, and DLQ.",
        "diffs": [
            {
                "path": "apps/api/app/workers/gmail_ingest_worker.py",
                "description": "Added bounded retries with exponential backoff and structured logging.",
            }
        ],
        "metrics": {
            "ingest_latency_p95_seconds": 45.0,
            "ingest_error_rate": 0.004,
            "ingest_queue_depth_max": 120,
        },
        "notes": [
            "We defined SLO: 95% ingest <= 2 minutes; error rate < 1%.",
            "We added a reconciliation job to repair index drift once per hour."
        ],
    }
    
    payload = {
        "boss_slug": "applylens-runtime-boss",
        "rubric_id": rubric.id,
        "player": {
            "id": "user_123",
            "name": "Test Player",
            "level": 5,
        },
        "run": {
            "id": 1,
            "attempt_index": 1,
        },
        "submission": submission_context,
    }
    
    print("\n" + "-" * 60)
    print("Submission Context:")
    print(f"  Summary: {submission_context['summary']}")
    print(f"  Metrics: ingest_error_rate = {submission_context['metrics']['ingest_error_rate']}")
    print(f"  Notes: {len(submission_context['notes'])} items")
    
    # Check if mock mode
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        print("\n⚠️  Running in MOCK mode (set EVALFORGE_MOCK_GRADING=0 for real ZERO)")
        choice_data = {
            "dimensions": [
                {"key": "slo_and_metrics", "level": 2, "rationale": "SLO defined with basic alerting"},
                {"key": "observability_pipeline", "level": 2, "rationale": "Per-stage metrics with thread IDs"},
                {"key": "failure_handling", "level": 2, "rationale": "Bounded retries with backoff"},
                {"key": "idempotency_and_consistency", "level": 1, "rationale": "Basic idempotency checks"},
                {"key": "alerts_and_response", "level": 1, "rationale": "Some alerts but noisy"},
                {"key": "load_testing_and_drills", "level": 1, "rationale": "Ad-hoc testing only"},
            ],
            "autofail_conditions_triggered": []
        }
        choice = BossEvalLLMChoice.model_validate(choice_data)
    else:
        # Real ZERO call
        print("\n🤖 Calling ZERO (this may take a few seconds)...")
        zero_resp = call_zero_boss_judge(rubric=rubric, payload=payload)
        choice = BossEvalLLMChoice.model_validate(zero_resp)
    
    # Score the evaluation
    result = score_boss_eval(rubric, choice)
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULT")
    print("=" * 60)
    print(f"Total Score: {result.total_score} / {result.max_score}")
    print(f"Grade: {result.grade}")
    print(f"Autofail: {result.autofail_triggered}")
    
    print("\nPer-Dimension Breakdown:")
    for dim_result in result.dimensions:
        print(f"\n  [{dim_result.key}]")
        print(f"    Level: {dim_result.level} ({dim_result.band_label})")
        print(f"    Score: {dim_result.band_score}")
        print(f"    Rationale: {dim_result.rationale}")
    
    return result


async def example_intent_oracle():
    """Example: Judge the Intent Oracle (agent boss) submission."""
    from arcade_app.boss_rubric_helper import load_boss_rubric, score_boss_eval
    from arcade_app.boss_rubric_models import BossEvalLLMChoice
    
    print("\n\n" + "=" * 60)
    print("EXAMPLE: Intent Oracle (Agent Boss)")
    print("=" * 60)
    
    # Load the rubric
    rubric = load_boss_rubric("applylens_agent_boss")
    print(f"\nRubric: {rubric.title}")
    print(f"Autofail Conditions: {rubric.autofail_conditions}")
    
    # Construct submission context
    submission_context = {
        "summary": "Triage agent with Judge/Coach eval loop and basic safety guardrails.",
        "intent_taxonomy": {
            "labels": ["interview_invite", "offer", "rejection", "application_update", "other"],
            "documented": True,
        },
        "benchmark": {
            "examples_count": 25,
            "accuracy": 0.84,
            "confusion_points": ["Generic follow-ups vs action-required"],
        },
        "safety": {
            "policy_rules": ["no_auto_reply", "flag_security_alerts"],
            "violations_detected": 0,
        },
        "notes": [
            "Benchmark set includes 5 ambiguous cases where humans disagree.",
            "Agent exposes confidence levels (low/medium/high) in responses.",
        ],
    }
    
    # Mock a good-but-not-perfect score
    choice_data = {
        "dimensions": [
            {"key": "intent_taxonomy", "level": 2, "rationale": "Clear taxonomy with well-defined outcomes"},
            {"key": "benchmark_and_eval", "level": 2, "rationale": "Structured eval with labeled examples"},
            {"key": "suggestion_quality", "level": 2, "rationale": "84% accuracy, generally helpful"},
            {"key": "safety_and_policy", "level": 2, "rationale": "Policies encoded and enforced"},
            {"key": "uncertainty_handling", "level": 2, "rationale": "Explicit confidence levels"},
            {"key": "observability_and_regressions", "level": 1, "rationale": "Basic metrics tracked"},
        ],
        "autofail_conditions_triggered": []  # No policy violations
    }
    
    choice = BossEvalLLMChoice.model_validate(choice_data)
    result = score_boss_eval(rubric, choice)
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULT")
    print("=" * 60)
    print(f"Total Score: {result.total_score} / {result.max_score}")
    print(f"Grade: {result.grade}")
    
    return result


async def main():
    """Run both examples."""
    print("\n🎮 ZERO Boss Judge Examples for ApplyLens\n")
    
    # Example 1: Runtime boss
    await example_inbox_maelstrom()
    
    # Example 2: Agent boss
    await example_intent_oracle()
    
    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
