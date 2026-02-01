"""
Tests for Phase 8.x Boss Judge Schema Validation (Fail-Closed).

Ensures that boss judge responses are strictly validated and failures
are handled gracefully with proper error codes and metadata.
"""
import pytest
import json
from arcade_app.schemas.boss_judge import parse_boss_judge_result, BossJudgeResult


def test_valid_judge_result_parses():
    """Valid JSON with all required fields parses successfully."""
    valid_json = """
    {
      "pass": true,
      "score": 85,
      "rubric_breakdown": [
        {
          "criterion": "Code Quality",
          "score": 90,
          "evidence": ["Clean code", "Good naming"]
        }
      ],
      "blocking_issues": [],
      "recommendations": ["Add tests"],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    """
    
    result = parse_boss_judge_result(valid_json, "gemini-2.5-flash-001", "boss-judge-v1")
    assert result.pass_ == True
    assert result.score == 85
    assert len(result.rubric_breakdown) == 1
    assert result.rubric_breakdown[0].criterion == "Code Quality"
    assert result.model_id == "gemini-2.5-flash-001"


def test_invalid_json_raises_error():
    """Invalid JSON raises ValueError."""
    invalid_json = "This is not JSON at all"
    
    with pytest.raises(ValueError, match="No valid JSON found"):
        parse_boss_judge_result(invalid_json, "model", "v1")


def test_json_with_extra_fields_rejected():
    """Extra fields are rejected (extra='forbid')."""
    json_with_extra = """
    {
      "pass": true,
      "score": 85,
      "rubric_breakdown": [],
      "blocking_issues": [],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z",
      "extra_field_should_fail": "invalid"
    }
    """
    
    with pytest.raises(ValueError, match="Schema validation failed"):
        parse_boss_judge_result(json_with_extra, "model", "v1")


def test_missing_required_fields_rejected():
    """Missing required fields raise error."""
    json_missing_score = """
    {
      "pass": true,
      "rubric_breakdown": [],
      "blocking_issues": [],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    """
    
    with pytest.raises(ValueError, match="Schema validation failed"):
        parse_boss_judge_result(json_missing_score, "model", "v1")


def test_score_bounds_enforced():
    """Score must be 0-100."""
    json_invalid_score = """
    {
      "pass": true,
      "score": 150,
      "rubric_breakdown": [],
      "blocking_issues": [],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    """
    
    with pytest.raises(ValueError, match="Schema validation failed"):
        parse_boss_judge_result(json_invalid_score, "model", "v1")


def test_rubric_row_score_bounds():
    """Rubric row scores must be 0-100."""
    json_invalid_rubric_score = """
    {
      "pass": true,
      "score": 85,
      "rubric_breakdown": [
        {
          "criterion": "Test",
          "score": 200,
          "evidence": []
        }
      ],
      "blocking_issues": [],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    """
    
    with pytest.raises(ValueError, match="Schema validation failed"):
        parse_boss_judge_result(json_invalid_rubric_score, "model", "v1")


def test_metadata_auto_added_if_missing():
    """Parser adds metadata fields if missing from response."""
    json_without_metadata = """
    {
      "pass": false,
      "score": 50,
      "rubric_breakdown": [],
      "blocking_issues": ["Issue 1"],
      "recommendations": []
    }
    """
    
    result = parse_boss_judge_result(json_without_metadata, "test-model", "test-v1")
    assert result.model_id == "test-model"
    assert result.prompt_version == "test-v1"
    assert result.judged_at is not None  # Auto-generated


def test_fail_closed_zero_score():
    """Fail-closed response has score=0."""
    fail_json = """
    {
      "pass": false,
      "score": 0,
      "rubric_breakdown": [
        {
          "criterion": "All",
          "score": 0,
          "evidence": ["Judge schema validation failed"]
        }
      ],
      "blocking_issues": ["E_JUDGE_SCHEMA"],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    """
    
    result = parse_boss_judge_result(fail_json, "model", "v1")
    assert result.pass_ == False
    assert result.score == 0
    assert "E_JUDGE_SCHEMA" in result.blocking_issues


def test_markdown_json_extraction():
    """Parser can extract JSON from markdown code blocks."""
    markdown_json = """
    Here's the evaluation:
    
    ```json
    {
      "pass": true,
      "score": 75,
      "rubric_breakdown": [],
      "blocking_issues": [],
      "recommendations": [],
      "model_id": "gemini-2.5-flash-001",
      "prompt_version": "boss-judge-v1",
      "judged_at": "2026-01-31T19:00:00Z"
    }
    ```
    
    Hope that helps!
    """
    
    result = parse_boss_judge_result(markdown_json, "model", "v1")
    assert result.score == 75
    assert result.pass_ == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
