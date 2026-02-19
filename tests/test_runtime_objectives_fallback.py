
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from arcade_app.services.quest_validate import validate_quest_attempt, ObjResult
from arcade_app.services.coach_service import coach_service
from arcade_app.schemas.coach_schemas import CoachRequest

class TestRuntimeFallback(unittest.TestCase):

    def test_invalid_objective_schema_returns_config_error(self):
        """C1: Validation preflight should catch invalid schema."""
        
        # Mock quest definition with invalid objective
        # Using a dict to simulate what validate_quest_attempt expects for quest_def
        # It uses getattr, so an object or dict with attribute access or keys?
        # validate_quest_attempt uses getattr(quest_def, "objectives_json", [])
        # So I need an object or a mock.
        
        quest_def = MagicMock()
        quest_def.objectives_json = [
            {"id": "obj1", "kind": "unknown_kind", "rule": {"a": 1}} 
        ]
        quest_def.slug = "test-quest"

        results = validate_quest_attempt(
            code="print('hello')",
            stdout="hello",
            stderr="",
            quest_def=quest_def
        )

        self.assertEqual(len(results), 1)
        res = results[0]
        self.assertEqual(res["id"], "CONFIG_INVALID_OBJECTIVES")
        self.assertEqual(res["kind"], "config")
        self.assertIn("Unknown kind 'unknown_kind'", res["actual"])
        self.assertIn("Hint: Run --validate-only", res["diff"])

    def test_missing_field_in_objective(self):
        """C1: Validation preflight should catch missing rule field."""
        
        quest_def = MagicMock()
        quest_def.objectives_json = [
            # stdout_exact requires 'expected'
            {"id": "obj1", "kind": "stdout_exact", "rule": {"foo": "bar"}} 
        ]
        quest_def.slug = "test-quest"

        results = validate_quest_attempt(
            code="print('hello')",
            stdout="hello",
            stderr="",
            quest_def=quest_def
        )

        res = results[0]
        self.assertEqual(res["id"], "CONFIG_INVALID_OBJECTIVES")
        self.assertIn("Rule missing required field 'expected'", res["actual"])

    def test_coach_short_circuit_on_config_error(self):
        """C2: Coach should short-circuit if runner_result has config error."""
        
        # Construct a request with a config error in runner_result
        runner_result = {
            "objectives": [
                {
                    "id": "CONFIG_INVALID_OBJECTIVES",
                    "kind": "config",
                    "ok": False,
                    "detail": "Invalid Quest Configuration",
                    "actual": "Missing 'kind'",
                    "diff": "Hint: Run --validate-only"
                }
            ]
        }
        
        req = CoachRequest(
            mode="auto",
            world="test-world",
            quest_slug="test-quest",
            student_mode=False,
            runner_result=runner_result,
            failing_tests_text="",
            terminal_output_text="",
            workspace_files=[]
        )
        
        # We don't need to mock Gemini client if short-circuit works, 
        # but to be safe we mock client to ensure it is NOT called.
        coach_service.client = MagicMock()
        
        # Run async test (using unittest.IsolatedAsyncioTestCase if available, or just asyncio.run)
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        response = loop.run_until_complete(coach_service.process_request(req))
        
        # Assertions
        self.assertIn("Coach Service Unavailable", response.summary_md)
        self.assertIn("Quest Configuration Error", response.summary_md)
        self.assertIn("Missing 'kind'", response.summary_md)
        self.assertIn("--validate-only", response.summary_md)
        
        # Verify Gemini was NOT called
        if hasattr(coach_service.client.models, 'generate_content'):
             coach_service.client.models.generate_content.assert_not_called()

if __name__ == '__main__':
    unittest.main()
