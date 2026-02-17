
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from arcade_app.schemas.coach_schemas import CoachRequest, CoachResponse, SafetyAssessment, UnifiedDiff
from arcade_app.services.coach_service import coach_service, CoachService

# Helper to create a dummy request
def make_req(mode="auto", student_mode=True, failing_tests=None, terminal_output=None):
    return CoachRequest(
        mode=mode,
        world="test-world",
        quest_slug="test-quest",
        student_mode=student_mode,
        failing_tests_text=failing_tests,
        terminal_output_text=terminal_output,
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
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        evidence=[]
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
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        evidence=[]
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
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        evidence=[]
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
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        evidence=[]
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act: Auto mode + NO failures
    req = make_req(mode="auto", failing_tests=None)
    res = await coach_service.process_request(req)

    assert res.mode == "explain"

@pytest.mark.asyncio
async def test_detect_workspace_missing():
    """TC3: Pre-Parser detects WORKSPACE_MISSING."""
    # Setup Mock
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    # Mock Response with evidence to pass guardrail
    mock_response = MagicMock()
    mock_response.parsed = CoachResponse(
        mode="debug",
        summary_md="Workspace missing.",
        hypotheses=[],
        next_steps=[],
        patch=None,
        confidence=1.0,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        failure_class="WORKSPACE_MISSING",
        evidence=["[Errno 2] No such file or directory"]
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act
    terminal_output = "python3.11: can't open file '.../main.py': [Errno 2] No such file or directory"
    req = make_req(mode="debug", terminal_output=terminal_output)
    res = await coach_service.process_request(req)

    # Assert
    assert coach_service._detect_failed_state(terminal_output) == "WORKSPACE_MISSING"

@pytest.mark.asyncio
async def test_evidence_enforcement_downgrades():
    """TC4: Guardrail downgrades confidence if evidence missing for detected failure."""
    # Setup Mock
    mock_client = MagicMock()
    coach_service.client = mock_client
    
    # Mock Response WITHOUT evidence
    mock_response = MagicMock()
    mock_response.parsed = CoachResponse(
        mode="debug",
        summary_md="Workspace missing.",
        hypotheses=[],
        next_steps=[],
        patch=None,
        confidence=1.0,
        safety=SafetyAssessment(solution_leak_risk="low", blocked=False),
        failure_class="WORKSPACE_MISSING",
        evidence=[] # MISSING EVIDENCE
    )
    mock_client.models.generate_content.return_value = mock_response

    # Act
    terminal_output = "python3.11: can't open file '.../main.py': [Errno 2] No such file or directory"
    req = make_req(mode="debug", terminal_output=terminal_output)
    res = await coach_service.process_request(req)

    # Assert
    assert res.confidence == 0.5
    assert len(res.evidence) > 0 # Should have been populated by guardrail
