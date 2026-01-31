"""
Test suite for grading math and weighted scoring logic.
Verifies that rubric weights are applied correctly.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arcade_app.grading_helper import (
    RubricConfig,
    DEFAULT_RUBRIC,
    DEBUGGING_RUBRIC,
    _grade_submission_internal
)
from arcade_app.session_state import SessionState


# --- Unit Tests for Math ---

def test_calculate_weighted_score_default():
    """Test weighted scoring with default rubric (40/40/20)."""
    # Scenario: Good logic (5), Bad docs (1), Messy (2)
    scores = {"coverage": 1, "correctness": 5, "clarity": 2}
    
    # Default Rubric: Cov(0.4), Corr(0.4), Clar(0.2)
    # Math: (1*0.4 + 5*0.4 + 2*0.2) / 5.0 = 2.8 / 5.0 = 0.56 -> 56.0
    result = DEFAULT_RUBRIC.calculate_score(scores)
    assert result == 56.0


def test_calculate_weighted_score_debugging():
    """Test weighted scoring with debugging rubric (30/50/20)."""
    # Same scores, different rubric
    scores = {"coverage": 1, "correctness": 5, "clarity": 2}
    
    # Debugging Rubric: Cov(0.3), Corr(0.5), Clar(0.2)
    # Math: (1*0.3 + 5*0.5 + 2*0.2) / 5.0 = 3.2 / 5.0 = 0.64 -> 64.0
    result = DEBUGGING_RUBRIC.calculate_score(scores)
    assert result == 64.0


def test_perfect_score():
    """Test that perfect scores yield 100.0."""
    scores = {"coverage": 5, "correctness": 5, "clarity": 5}
    result = DEFAULT_RUBRIC.calculate_score(scores)
    assert result == 100.0


def test_zero_score():
    """Test that zero scores yield 0.0."""
    scores = {"coverage": 0, "correctness": 0, "clarity": 0}
    result = DEFAULT_RUBRIC.calculate_score(scores)
    assert result == 0.0


# --- Integration Mock Test (Async) ---

@pytest.mark.asyncio
async def test_grade_submission_flow():
    """Test the full grading flow with mocked Vertex AI."""
    # Mock the Vertex AI Model
    mock_model = MagicMock()
    
    # Mock the async generation to return a JSON string
    mock_response = MagicMock()
    mock_response.text = '{"coverage": 3, "correctness": 4, "clarity": 4, "comment": "Good job"}'
    
    # Setup the awaitable on the mock
    future = asyncio.Future()
    future.set_result(mock_response)
    mock_model.generate_content_async.return_value = future

    # Create a mock session state
    state = SessionState(track="debugging")
    
    # Patch vertexai.init and GenerativeModel
    import arcade_app.grading_helper as gh
    original_init = gh.vertexai.init
    original_model_class = gh.GenerativeModel
    
    gh.vertexai.init = MagicMock()
    gh.GenerativeModel = MagicMock(return_value=mock_model)
    
    try:
        # Run the function
        result = await _grade_submission_internal(
            "print('hello')", 
            state, 
            DEBUGGING_RUBRIC
        )

        # Assertions
        assert result["coverage"] == 3
        assert result["correctness"] == 4
        assert result["clarity"] == 4
        assert result["comment"] == "Good job"
        
        # Check Math for 3, 4, 4 on Debugging rubric
        # (3*0.3 + 4*0.5 + 4*0.2) / 5 = (0.9 + 2.0 + 0.8) / 5 = 3.7 / 5 = 74.0
        weighted = DEBUGGING_RUBRIC.calculate_score(result)
        assert weighted == 74.0
        
    finally:
        # Restore
        gh.vertexai.init = original_init
        gh.GenerativeModel = original_model_class


def test_rubric_weights_sum():
    """Ensure rubric weights sum to 1.0 for consistency."""
    assert sum(DEFAULT_RUBRIC.weights.values()) == pytest.approx(1.0)
    assert sum(DEBUGGING_RUBRIC.weights.values()) == pytest.approx(1.0)
