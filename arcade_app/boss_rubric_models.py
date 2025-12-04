# arcade_app/boss_rubric_models.py
"""
Pydantic models for boss rubrics and evaluation results.
Used by the boss judge system to load rubrics, score evaluations, and return structured results.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class BossRubricBand(BaseModel):
    level: int
    label: str
    score: int
    criteria: str


class BossRubricDimension(BaseModel):
    key: str
    label: str
    weight: float
    description: str
    bands: List[BossRubricBand]


class BossRubricGradeBand(BaseModel):
    min_score: int
    label: str
    description: str


class BossRubric(BaseModel):
    schema_version: str
    id: str
    boss_slug: str
    title: str
    max_score: int
    dimensions: List[BossRubricDimension]
    grade_bands: List[BossRubricGradeBand]
    autofail_conditions: List[str]
    llm_judge_instructions: str


class BossEvalDimensionChoice(BaseModel):
    """ZERO's choice for a single dimension."""
    key: str
    level: int
    rationale: str


class BossEvalLLMChoice(BaseModel):
    """What ZERO returns after reading code/docs/metrics + rubric."""
    dimensions: List[BossEvalDimensionChoice]
    autofail_conditions_triggered: List[str] = []


class BossEvalDimensionResult(BaseModel):
    """Scored result for a single dimension."""
    key: str
    label: str
    level: int
    band_label: str
    band_score: int
    rationale: str


class BossEvalResult(BaseModel):
    """Final evaluation result for a boss encounter."""
    boss_slug: str
    rubric_id: str
    total_score: int
    grade: str
    max_score: int
    autofail_triggered: bool
    autofail_reasons: List[str]
    dimensions: List[BossEvalDimensionResult]

    # Optional combat overlay fields (can be filled by caller)
    boss_hp_before: Optional[int] = None
    boss_hp_after: Optional[int] = None
    boss_hp_delta: Optional[int] = None
    integrity_before: Optional[int] = None
    integrity_after: Optional[int] = None
    integrity_delta: Optional[int] = None
