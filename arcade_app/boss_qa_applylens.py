# arcade_app/boss_qa_applylens.py
"""
QA helper for ApplyLens boss evaluations.
Runs structured tests against Inbox Maelstrom and Intent Oracle using ZERO + rubrics.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .boss_rubric_models import BossEvalResult
from .grading_helper import judge_boss_with_rubric
from .models import BossDefinition, BossRun, Profile


class BossQAStatus(BaseModel):
    boss_slug: str
    rubric_id: str
    score: int
    grade: str
    min_score_required: int
    passed: bool
    boss_hp_before: int
    boss_hp_after: int
    boss_hp_delta: int
    integrity_before: int
    integrity_after: int
    integrity_delta: int


class ApplyLensBossQAReport(BaseModel):
    project_slug: str = "applylens"
    results: List[BossQAStatus]
    overall_pass: bool


def _get_boss(db: Session, slug: str) -> BossDefinition:
    boss = (
        db.query(BossDefinition)
        .filter(BossDefinition.id == slug)
        .one_or_none()
    )
    if boss is None:
        raise ValueError(f"BossDefinition not found for slug={slug}")
    return boss


def _run_single_boss_qa(
    db: Session,
    boss: BossDefinition,
    player: Profile,
    min_score_required: int,
    submission_context: dict,
) -> BossQAStatus:
    """Run QA for a single boss."""
    # Create a fresh BossRun for QA
    run = BossRun(
        boss_id=boss.id,
        profile_id=player.id,
        attempt=1,
        boss_hp=boss.max_hp,
    )
    db.add(run)
    db.flush()

    eval_result: BossEvalResult = judge_boss_with_rubric(
        boss=boss,
        run=run,
        player=player,
        submission_context=submission_context,
    )

    score = eval_result.total_score
    grade = eval_result.grade
    passed = score >= min_score_required and not eval_result.autofail_triggered

    boss_hp_before = eval_result.boss_hp_before or boss.max_hp
    boss_hp_after = eval_result.boss_hp_after or boss_hp_before
    boss_hp_delta = eval_result.boss_hp_delta or 0

    integrity_before = eval_result.integrity_before or player.integrity
    integrity_after = eval_result.integrity_after or integrity_before
    integrity_delta = eval_result.integrity_delta or 0

    return BossQAStatus(
        boss_slug=boss.id,
        rubric_id=eval_result.rubric_id,
        score=score,
        grade=grade,
        min_score_required=min_score_required,
        passed=passed,
        boss_hp_before=boss_hp_before,
        boss_hp_after=boss_hp_after,
        boss_hp_delta=boss_hp_delta,
        integrity_before=integrity_before,
        integrity_after=integrity_after,
        integrity_delta=integrity_delta,
    )


def run_applylens_boss_qa(
    db: Session,
    player: Profile,
    min_score_runtime: int = 60,
    min_score_agent: int = 60,
) -> ApplyLensBossQAReport:
    """
    Run a full QA pass for ApplyLens bosses using ZERO + rubrics.

    Returns a structured report that can be used by dev routes and CLI.
    """
    # Boss slugs as defined in the ApplyLens questline/boss spec
    runtime_slug = "applylens-runtime-boss"
    agent_slug = "applylens-agent-boss"

    runtime_submission = {
        "summary": "ApplyLens runtime hardened against storm conditions.",
        "diffs": [
            {
                "path": "apps/api/app/workers/gmail_ingest_worker.py",
                "description": "Added bounded retries, timeouts, and structured logging for Gmail and Elasticsearch calls.",
            }
        ],
        "metrics": {
            "ingest_latency_p95_seconds": 45.0,
            "ingest_error_rate": 0.004,
            "ingest_queue_depth_max": 120,
        },
        "notes": [
            "Defined SLO: 95% of threads ingested+indexed within 2 minutes.",
            "Error rate alert when >1% over a 5-minute window.",
            "Dashboards show stage latencies and queue depth.",
            "Periodic reconciliation job compares DB vs index and re-enqueues missing docs.",
        ],
    }

    agent_submission = {
        "summary": "ApplyLens triage agent with intent taxonomy, eval harness, and safety guardrails.",
        "intent_taxonomy": [
            "interview_invite",
            "offer",
            "rejection",
            "application_update",
            "networking",
            "marketing",
            "security_alert",
            "other",
        ],
        "benchmark": {
            "total_examples": 40,
            "intents_covered": [
                "interview_invite",
                "offer",
                "rejection",
                "security_alert",
                "marketing",
            ],
        },
        "eval_results": {
            "accuracy_overall": 0.88,
            "accuracy_high_impact": 0.92,
            "policy_violations": 0,
        },
        "safety": {
            "policies": [
                "never auto-reply to security_alert",
                "never send emails automatically",
                "treat ambiguous security emails as high risk",
            ],
            "risk_handling": "High-risk messages are classified conservatively and routed for manual review.",
        },
        "notes": [
            "Judge/Coach harness runs on a curated set of labeled threads.",
            "Confidence is exposed (low/medium/high) and low confidence suggestions are downgraded or withheld.",
            "Prompt and tool changes go through an eval run before deploy.",
        ],
    }

    results: List[BossQAStatus] = []
    
    # Try runtime boss
    try:
        runtime_boss = _get_boss(db, runtime_slug)
        runtime_status = _run_single_boss_qa(
            db=db,
            boss=runtime_boss,
            player=player,
            min_score_required=min_score_runtime,
            submission_context=runtime_submission,
        )
        results.append(runtime_status)
    except ValueError:
        # Boss not found - graceful failure
        results.append(BossQAStatus(
            boss_slug=runtime_slug,
            rubric_id="N/A",
            score=0,
            grade="MISSING",
            min_score_required=min_score_runtime,
            passed=False,
            boss_hp_before=0,
            boss_hp_after=0,
            boss_hp_delta=0,
            integrity_before=0,
            integrity_after=0,
            integrity_delta=0,
        ))
    
    # Try agent boss
    try:
        agent_boss = _get_boss(db, agent_slug)
        agent_status = _run_single_boss_qa(
            db=db,
            boss=agent_boss,
            player=player,
            min_score_required=min_score_agent,
            submission_context=agent_submission,
        )
        results.append(agent_status)
    except ValueError:
        # Boss not found - graceful failure
        results.append(BossQAStatus(
            boss_slug=agent_slug,
            rubric_id="N/A",
            score=0,
            grade="MISSING",
            min_score_required=min_score_agent,
            passed=False,
            boss_hp_before=0,
            boss_hp_after=0,
            boss_hp_delta=0,
            integrity_before=0,
            integrity_after=0,
            integrity_delta=0,
        ))

    overall_pass = all(r.passed for r in results)

    return ApplyLensBossQAReport(results=results, overall_pass=overall_pass)
