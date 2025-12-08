# arcade_app/boss_qa_worlds.py
"""
QA helper for standard world bosses (Reactor Core, Signal Prism, etc.).
Provides structured testing for core world bosses using ZERO + rubrics.
"""
from __future__ import annotations

from typing import List, Dict, Any

from pydantic import BaseModel
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from arcade_app.boss_qa_applylens import BossQAStatus  # reuse the same shape
from arcade_app.boss_rubric_models import BossEvalResult
from arcade_app.grading_helper import judge_boss_with_rubric
from arcade_app.models import BossDefinition, BossRun, Profile


class WorldBossQARequest(BaseModel):
    boss_id: str | None = None
    world_slug: str | None = None
    submission_markdown: str | None = None
    mode: str | None = None 

class WorldBossQAReport(BaseModel):
    label: str = "worlds-fundamentals"
    results: List[BossQAStatus]
    overall_pass: bool


async def _get_boss(db: AsyncSession, slug: str) -> BossDefinition:
    stmt = select(BossDefinition).where(BossDefinition.id == slug)
    result = await db.exec(stmt)
    boss = result.one_or_none()
    
    if boss is None:
        raise ValueError(f"BossDefinition not found for slug={slug}")
    return boss


async def _run_single_boss_world_qa(
    db: AsyncSession,
    boss: BossDefinition,
    player: Profile,
    min_score_required: int,
    submission_context: Dict[str, Any],
) -> BossQAStatus:
    """Run QA for a single world boss."""
    # Fresh BossRun for QA
    run = BossRun(
        boss_id=boss.id,
        user_id=player.user_id,
        attempt=1,
        boss_hp=boss.max_hp,
    )
    db.add(run)
    await db.flush()

    eval_result: BossEvalResult = await judge_boss_with_rubric(
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
        criteria=[
            {"id": d.key, "score": d.band_score, "feedback": d.rationale}
            for d in eval_result.dimensions
        ],
        summary=eval_result.summary,
        strengths=eval_result.strengths,
        improvements=eval_result.improvements,
    )


async def run_standard_world_boss_qa(
    db: AsyncSession,
    player: Profile,
    min_scores: Dict[str, int] | None = None,
    request: WorldBossQARequest | None = None,
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
        {
            "boss_slug": "boss-grid-containment-sandbox-warden",
            "default_min_score": 6,
            "submission_context": {
                "summary": "Sandbox Warden Infra boss solution.",
                "files": ["runbook.md"],
                "notes": ["Checks triage, logs, and fix verification."],
            },
        },
    ]

    # If a specific boss is requested, filter the config or create a custom one
    if request and request.boss_id:
        # Check if we have a config for this boss
        matching_cfg = next((c for c in configs if c["boss_slug"] == request.boss_id), None)
        
        if request.submission_markdown:
            # Create a custom config or override existing
            custom_cfg = {
                "boss_slug": request.boss_id,
                "default_min_score": 6, # Default for rubric-based pass/fail
                "submission_context": {
                    "summary": "Smoke Test Runbook",
                    "files": ["runbook.md"],
                    "submission_markdown": request.submission_markdown,
                    "code": request.submission_markdown, # Ensure 'code' key is present for mock grader checks
                    # The judge logic needs to handle this.
                    # Usually 'judge_boss_with_rubric' expects 'submission_context' to have what the prompt needs.
                    # For ZERO prompts, we might inject this as the 'Player Runbook'.
                }
            }
            # Update 'submission_markdown' into context so 'judge_boss_with_rubric' sees it
            # We trust 'judge_boss_with_rubric' to use 'submission_markdown' key if present.
            configs = [custom_cfg]
        elif matching_cfg:
             configs = [matching_cfg]
        else:
             # Fallback: Try to run it even if not in hardcoded list (assuming DB has it)
             configs = [{
                "boss_slug": request.boss_id,
                "default_min_score": 6,
                "submission_context": {"summary": "Ad-hoc Execution"} 
             }]

    results: List[BossQAStatus] = []

    for cfg in configs:
        slug = cfg["boss_slug"]
        min_score_required = min_scores.get(slug, cfg["default_min_score"])
        
        try:
            boss = await _get_boss(db, slug)
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
        
        status = await _run_single_boss_world_qa(
            db=db,
            boss=boss,
            player=player,
            min_score_required=min_score_required,
            submission_context=cfg["submission_context"],
        )
        results.append(status)

    overall_pass = all(r.passed for r in results)

    return WorldBossQAReport(results=results, overall_pass=overall_pass)
