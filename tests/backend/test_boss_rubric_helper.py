"""
Unit tests for boss rubric helper.
Verifies that rubric loading and scoring logic works correctly.
"""
from arcade_app.boss_rubric_models import (
    BossRubric,
    BossEvalLLMChoice,
    BossEvalDimensionChoice,
)
from arcade_app.boss_rubric_helper import score_boss_eval


def test_score_boss_eval_basic():
    """Test basic scoring with two dimensions."""
    rubric_data = {
        "schema_version": "1.0",
        "id": "test_boss",
        "boss_slug": "test-boss",
        "title": "Test Boss Rubric",
        "max_score": 100,
        "dimensions": [
            {
                "key": "foo",
                "label": "Foo Dimension",
                "weight": 0.5,
                "description": "Test",
                "bands": [
                    {"level": 0, "label": "Bad", "score": 0, "criteria": "bad"},
                    {"level": 1, "label": "Ok", "score": 10, "criteria": "ok"},
                    {"level": 2, "label": "Good", "score": 20, "criteria": "good"},
                ],
            },
            {
                "key": "bar",
                "label": "Bar Dimension",
                "weight": 0.5,
                "description": "Test",
                "bands": [
                    {"level": 0, "label": "Bad", "score": 0, "criteria": "bad"},
                    {"level": 1, "label": "Ok", "score": 10, "criteria": "ok"},
                    {"level": 2, "label": "Good", "score": 20, "criteria": "good"},
                ],
            },
        ],
        "grade_bands": [
            {"min_score": 30, "label": "S", "description": ""},
            {"min_score": 10, "label": "B", "description": ""},
            {"min_score": 0, "label": "F", "description": ""},
        ],
        "autofail_conditions": [],
        "llm_judge_instructions": "ignore",
    }
    rubric = BossRubric.model_validate(rubric_data)

    choice = BossEvalLLMChoice(
        dimensions=[
            BossEvalDimensionChoice(key="foo", level=2, rationale="good foo"),
            BossEvalDimensionChoice(key="bar", level=1, rationale="ok bar"),
        ],
        autofail_conditions_triggered=[],
    )

    result = score_boss_eval(rubric, choice)

    assert result.total_score == 30  # 20 + 10
    assert result.grade == "S"
    assert len(result.dimensions) == 2
    assert result.dimensions[0].band_label == "Good"
    assert result.dimensions[1].band_label == "Ok"
    assert not result.autofail_triggered


def test_score_boss_eval_with_autofail():
    """Test that autofail conditions override the score."""
    rubric_data = {
        "schema_version": "1.0",
        "id": "test_boss_autofail",
        "boss_slug": "test-boss-autofail",
        "title": "Test Boss Rubric with Autofail",
        "max_score": 100,
        "dimensions": [
            {
                "key": "safety",
                "label": "Safety",
                "weight": 1.0,
                "description": "Test",
                "bands": [
                    {"level": 0, "label": "Unsafe", "score": 0, "criteria": "unsafe"},
                    {"level": 1, "label": "Safe", "score": 50, "criteria": "safe"},
                ],
            },
        ],
        "grade_bands": [
            {"min_score": 40, "label": "A", "description": ""},
            {"min_score": 0, "label": "F", "description": ""},
        ],
        "autofail_conditions": ["policy_violation", "systemic_safety_failure"],
        "llm_judge_instructions": "ignore",
    }
    rubric = BossRubric.model_validate(rubric_data)

    # High score but with autofail condition
    choice = BossEvalLLMChoice(
        dimensions=[
            BossEvalDimensionChoice(key="safety", level=1, rationale="looks safe"),
        ],
        autofail_conditions_triggered=["policy_violation"],
    )

    result = score_boss_eval(rubric, choice)

    assert result.total_score == 0  # autofail resets score
    assert result.grade == "F"
    assert result.autofail_triggered
    assert "policy_violation" in result.autofail_reasons


def test_score_boss_eval_grade_mapping():
    """Test that scores correctly map to grade bands."""
    rubric_data = {
        "schema_version": "1.0",
        "id": "test_boss_grades",
        "boss_slug": "test-boss-grades",
        "title": "Test Boss Grade Mapping",
        "max_score": 100,
        "dimensions": [
            {
                "key": "quality",
                "label": "Quality",
                "weight": 1.0,
                "description": "Test",
                "bands": [
                    {"level": 0, "label": "Poor", "score": 0, "criteria": "poor"},
                    {"level": 1, "label": "Fair", "score": 50, "criteria": "fair"},
                    {"level": 2, "label": "Excellent", "score": 100, "criteria": "excellent"},
                ],
            },
        ],
        "grade_bands": [
            {"min_score": 90, "label": "S", "description": ""},
            {"min_score": 75, "label": "A", "description": ""},
            {"min_score": 60, "label": "B", "description": ""},
            {"min_score": 40, "label": "C", "description": ""},
            {"min_score": 0, "label": "F", "description": ""},
        ],
        "autofail_conditions": [],
        "llm_judge_instructions": "ignore",
    }
    rubric = BossRubric.model_validate(rubric_data)

    # Test various score levels
    test_cases = [
        (2, 100, "S"),  # Excellent
        (1, 50, "C"),   # Fair
        (0, 0, "F"),    # Poor
    ]

    for level, expected_score, expected_grade in test_cases:
        choice = BossEvalLLMChoice(
            dimensions=[
                BossEvalDimensionChoice(key="quality", level=level, rationale="test"),
            ],
        )
        result = score_boss_eval(rubric, choice)
        assert result.total_score == expected_score
        assert result.grade == expected_grade
