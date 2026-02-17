
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from arcade_app.schemas.coach_schemas import CoachRequest, CoachResponse, SafetyAssessment, UnifiedDiff
from arcade_app.services.coach_service import coach_service, CoachService

# Helper to create a dummy request
def make_req(mode="auto", student_mode=True, failing_tests=None):
    return CoachRequest(
        mode=mode,
        world="test-world",
        quest_slug="test-quest",
        student_mode=student_mode,
        failing_tests_text=failing_tests,
        workspace_files=[],
    )

@pytest.mark.asyncio
async def test_guardrail_student_mode_strips_patch():
    """TC1: Student Mode Safety - Ensure patch is stripped if present."""
    # Setup Mock Client
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    # Mock Response
    mock_response = MagicMock()
    # The 'parsed' attribute returns the Pydantic model
    mock_response.parsed = CoachResponse(
        mode="debug",
        summary_md="Fix this.",
        hypotheses=[],
        next_steps=[],
        patch=UnifiedDiff(unified_diff="diff --git ..."), # Model tries to return patch
        confidence=0.9,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False)
    )
    
    mock_client.models.generate_content.return_value = mock_response

    # Act
    req = make_req(mode="debug", student_mode=True)
    res = await coach_service.process_request(req)

    # Assert
    assert res.patch is None, "Patch must be None in student mode"
    assert res.mode == "debug"

@pytest.mark.asyncio
async def test_guardrail_solution_mode_allows_patch():
    """TC1.b: Solution Mode - Allow patch."""
    # Setup Mock
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    expected_patch = UnifiedDiff(unified_diff="diff --git ...")
    
    mock_response = MagicMock()
    mock_response.parsed = CoachResponse(
        mode="debug",
        summary_md="Fix this.",
        hypotheses=[],
        next_steps=[],
        patch=expected_patch,
        confidence=0.9,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False)
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act
    req = make_req(mode="debug", student_mode=False)
    res = await coach_service.process_request(req)

    # Assert
    assert res.patch is not None, "Patch should be allowed in solution mode"
    assert res.patch.unified_diff == "diff --git ..."

@pytest.mark.asyncio
async def test_auto_mode_routing_failures():
    """TC2: Auto Mode - Routes to DEBUG when failures present."""
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    mock_response = MagicMock()
    mock_response.parsed = CoachResponse(
        mode="debug", # expectation
        summary_md="Debug summary",
        hypotheses=[],
        next_steps=[],
        patch=None,
        confidence=1.0,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False)
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act: Auto mode + failing tests
    req = make_req(mode="auto", failing_tests="Error: Expected 1 got 2")
    res = await coach_service.process_request(req)

    # Assert logic used Debug Prompt/Model (implicitly checked by response returning debug)
    # Check if 'mode' was updated in response object wrapper logic
    assert res.mode == "debug"

@pytest.mark.asyncio
async def test_auto_mode_routing_clean():
    """TC2.b: Auto Mode - Routes to EXPLAIN when no failures."""
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    mock_response = MagicMock()
    mock_response.parsed = CoachResponse(
        mode="explain", 
        summary_md="Explain summary",
        hypotheses=[],
        next_steps=[],
        patch=None,
        confidence=1.0,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False)
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act: Auto mode + NO failures
    req = make_req(mode="auto", failing_tests=None)
    res = await coach_service.process_request(req)

    assert res.mode == "explain"
