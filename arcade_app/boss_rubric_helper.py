# arcade_app/boss_rubric_helper.py
"""
Helper module for loading boss rubrics and scoring evaluations.
Provides the core logic for converting LLM judge choices into structured scores and grades.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .boss_rubric_models import (
    BossRubric,
    BossEvalLLMChoice,
    BossEvalResult,
    BossEvalDimensionResult,
    BossRubricDimension,
)


RUBRIC_DIR = Path("rubrics")


def load_boss_rubric(rubric_id: str) -> BossRubric:
    """
    Load a boss rubric JSON by rubric_id.
    
    Args:
        rubric_id: The rubric identifier (e.g., 'applylens_runtime_boss')
        
    Returns:
        Parsed BossRubric object
        
    Raises:
        FileNotFoundError: If rubric file doesn't exist
    """
    # Support both direct filename and rubric_id format
    if rubric_id.endswith('.json'):
        path = RUBRIC_DIR / rubric_id
    else:
        # Try boss-{slug} format first (our actual naming)
        slug_format = rubric_id.replace('_', '-')
        path = RUBRIC_DIR / f"boss-{slug_format}.json"
        
        if not path.exists():
            # Fallback to direct rubric_id.json
            path = RUBRIC_DIR / f"{rubric_id}.json"
    
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    rubric = BossRubric.model_validate(data)
    return rubric


def score_boss_eval(rubric: BossRubric, choice: BossEvalLLMChoice) -> BossEvalResult:
    """
    Given a BossRubric + LLM choices (dimension key → band level),
    compute the total score + grade + per-dimension results.
    
    Args:
        rubric: The boss rubric defining dimensions and scoring
        choice: The LLM's dimension choices and any autofail triggers
        
    Returns:
        Complete evaluation result with score, grade, and breakdown
    """
    # Index rubric dimensions by key
    dim_index: Dict[str, BossRubricDimension] = {
        d.key: d for d in rubric.dimensions
    }

    # Score per dimension
    dim_results: list[BossEvalDimensionResult] = []
    total_score = 0

    for dim_choice in choice.dimensions:
        dim = dim_index.get(dim_choice.key)
        if dim is None:
            # Ignore unknown dimension keys to keep this robust
            continue

        # Find the band with matching level (fallback: lowest level)
        band = next(
            (b for b in dim.bands if b.level == dim_choice.level),
            min(dim.bands, key=lambda b: b.level),
        )

        total_score += band.score

        dim_results.append(
            BossEvalDimensionResult(
                key=dim.key,
                label=dim.label,
                level=dim_choice.level,
                band_label=band.label,
                band_score=band.score,
                rationale=dim_choice.rationale,
            )
        )

    # Clamp to rubric.max_score
    total_score = max(0, min(total_score, rubric.max_score))

    # Autofail?
    triggered = set(choice.autofail_conditions_triggered or [])
    autofail_reasons = sorted(triggered & set(rubric.autofail_conditions))

    autofail_triggered = len(autofail_reasons) > 0
    if autofail_triggered:
        total_score = 0  # hard reset on autofail

    # Map to grade band
    grade = _grade_for_score(rubric, total_score)

    return BossEvalResult(
        boss_slug=rubric.boss_slug,
        rubric_id=rubric.id,
        total_score=total_score,
        grade=grade,
        max_score=rubric.max_score,
        autofail_triggered=autofail_triggered,
        autofail_reasons=autofail_reasons,
        dimensions=dim_results,
    )


def _grade_for_score(rubric: BossRubric, score: int) -> str:
    """
    Map a numeric score to a grade band label.
    
    Args:
        rubric: The rubric containing grade bands
        score: The numeric score to map
        
    Returns:
        Grade label (e.g., 'S', 'A', 'B', 'C', 'F')
    """
    # grade_bands: pick the highest band whose min_score <= score
    best_label = "F"
    best_min = -1

    for band in rubric.grade_bands:
        if score >= band.min_score and band.min_score > best_min:
            best_min = band.min_score
            best_label = band.label

    return best_label
