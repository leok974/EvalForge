# arcade_app/boss_qa_worlds.py
"""
QA helper for standard world bosses (Reactor Core, Signal Prism, etc.).
Provides structured testing for core world bosses using ZERO + rubrics.
"""
from __future__ import annotations

from typing import List, Dict, Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from arcade_app.boss_qa_applylens import BossQAStatus  # reuse the same shape
from arcade_app.boss_rubric_models import BossEvalResult
from arcade_app.grading_helper import judge_boss_with_rubric
from arcade_app.models import BossDefinition, BossRun, Profile


class WorldBossQAReport(BaseModel):
    label: str = "worlds-fundamentals"
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


def _run_single_boss_world_qa(
    db: Session,
    boss: BossDefinition,
    player: Profile,
    min_score_required: int,
    submission_context: Dict[str, Any],
) -> BossQAStatus:
    """Run QA for a single world boss."""
    # Fresh BossRun for QA
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


def run_standard_world_boss_qa(
    db: Session,
    player: Profile,
    min_scores: Dict[str, int] | None = None,
) -> WorldBossQAReport:
    """
    Run a QA pass for the standard worlds bosses (e.g., Reactor Core, Signal Prism).

    min_scores: optional mapping boss_slug -> min_score_required.
                Defaults to 60 if not provided.
    """
    if min_scores is None:
        min_scores = {}

    # Boss configurations with submission contexts
    configs: List[Dict[str, Any]] = [
        {
            "boss_slug": "reactor-core",
            "default_min_score": 60,
            "submission_context": {
                "summary": "Reactor Core Python boss solution focusing on loops, state, and tests.",
                "files": [
                    "apps/exercises/reactor_core/main.py",
                    "apps/exercises/reactor_core/tests/test_reactor_core.py",
                ],
                "notes": [
                    "Implements the required core() function with correct state transitions.",
                    "Includes unit tests for all specified edge cases.",
                    "Code is readable and follows the style guidelines from the Codex.",
                ],
            },
        },
        {
            "boss_slug": "signal-prism",
            "default_min_score": 60,
            "submission_context": {
                "summary": "Signal Prism TypeScript boss solution focusing on reducer logic and immutability.",
                "files": [
                    "apps/exercises/signal_prism/reducer.ts",
                    "apps/exercises/signal_prism/tests/reducer.test.ts",
                ],
                "notes": [
                    "Implements a pure reducer with no side effects.",
                    "Handles all specified action types and invalid actions gracefully.",
                    "Includes tests that cover happy path and edge cases.",
                ],
            },
        },
        # Add more bosses here later (Archives, Grid, Oracle, etc.)
    ]

    results: List[BossQAStatus] = []

    for cfg in configs:
        slug = cfg["boss_slug"]
        min_score_required = min_scores.get(slug, cfg["default_min_score"])
        
        try:
            boss = _get_boss(db, slug)
        except ValueError:
            # Boss not found in database - return graceful failure
            results.append(BossQAStatus(
                boss_slug=slug,
                rubric_id="N/A",
                score=0,
                grade="MISSING",
                min_score_required=min_score_required,
                passed=False,
                boss_hp_before=0,
                boss_hp_after=0,
                boss_hp_delta=0,
                integrity_before=0,
                integrity_after=0,
                integrity_delta=0,
            ))
            continue
        
        status = _run_single_boss_world_qa(
            db=db,
            boss=boss,
            player=player,
            min_score_required=min_score_required,
            submission_context=cfg["submission_context"],
        )
        results.append(status)

    overall_pass = all(r.passed for r in results)

    return WorldBossQAReport(results=results, overall_pass=overall_pass)
