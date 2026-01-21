
import pytest
from unittest.mock import MagicMock, patch
from arcade_app.routers.routes_quests_runtime import run_quest
from arcade_app.schemas.quest_run import RunRequest, QuestRunPayload
from arcade_app.models import QuestAttempt

@pytest.mark.asyncio
async def test_run_quest_objective_results_serialization_regression():
    """
    Regression test: Ensure run_quest handles objective_results being a list of dicts
    WITHOUT calling .model_dump() on them, avoiding AttributeError.
    """
    # Mock dependencies
    mock_db = MagicMock()
    mock_quest_tracker = MagicMock()
    mock_prog = MagicMock()
    
    # Mock Quest
    mock_quest = MagicMock()
    mock_quest.slug = "test-quest"
    
    # Mock Attempt
    mock_attempt = MagicMock(spec=QuestAttempt)
    mock_attempt.quest_slug = "test-quest"
    
    # Payload
    payload = RunRequest(
        code="print('hello')",
        language="python"
    )
    
    # Mock Evaluator Response
    # CRITICAL: This mocks the return from execute_code/evaluate which returns dicts
    mock_eval_result = (
        0, # exit_code
        "output", # stdout
        "", # stderr
        True, # passed
        [{"name": "Test 1", "success": True}], # objective_results AS DICTS
        "Summary" # failure_summary
    )
    
    with patch("arcade_app.routers.routes_quests_runtime.Evaluator") as MockEvaluator, \
         patch("arcade_app.routers.routes_quests_runtime.verify_quest_availability") as mock_verify, \
         patch("arcade_app.routers.routes_quests_runtime.get_or_create_quest_attempt") as mock_get_attempt, \
         patch("arcade_app.routers.routes_quests_runtime.generate_quick_fixes") as mock_gen_fixes, \
         patch("arcade_app.routers.routes_quests_runtime.QuestAttempt.model_validate") as mock_model_validate: # Mock DB update
         
        mock_verify.return_value = (mock_quest, mock_prog)
        mock_get_attempt.return_value = mock_attempt
        
        # Setup Evaluator instance
        mock_eval_instance = MockEvaluator.return_value
        mock_eval_instance.evaluate_quest.return_value = mock_eval_result
        
        # Setup Quick Fix Generator to return empty list (not testing that logic here)
        mock_gen_fixes.return_value = []

        # Call the function under test
        response = await run_quest(
            quest_slug="test-quest",
            payload=payload,
            db=mock_db,
            quest_tracker=mock_quest_tracker,
            current_user=MagicMock()
        )
        
        # Assertions
        assert response["result"]["objective_results"] == [{"name": "Test 1", "success": True}]
        # The fact that it didn't raise AttributeError is the main success criterion.
