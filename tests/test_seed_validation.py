
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from arcade_app.seed_quests_standard_worlds import seed_standard_world_quests

class TestSeedValidation(unittest.TestCase):
    def test_invalid_objective_raises_error(self):
        # Mock DB
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.one_or_none.return_value = None
        
        # Mock config with invalid objective
        invalid_config = [{
            "slug": "test-quest",
            "world_id": "world-test",
            "track_id": "track-test",
            "order_index": 1,
            "title": "Test",
            "short_description": "Desc",
            "detailed_description": "Detailed",
            "rubric_id": "rubric",
            "starting_code_path": "path",
            "unlocks_boss_id": None,
            "unlocks_layout_id": None,
            "base_xp_reward": 10,
            "mastery_xp_bonus": 5,
            "objectives_json": [
                {
                    "id": "obj1",
                    "kind": "unknown_kind", # Invalid
                    "rule": {"foo": "bar"}
                }
            ]
        }]
        
        with patch('arcade_app.seed_quests_standard_worlds.STANDARD_QUESTLINES', invalid_config):
            with self.assertRaises(ValueError) as cm:
                seed_standard_world_quests(mock_db)
            
            self.assertIn("CRITICAL: Invalid Objective", str(cm.exception))
            self.assertIn("Unknown kind 'unknown_kind'", str(cm.exception))


    def test_validate_only_mode(self):
        # Mock DB (should not be used)
        mock_db = MagicMock()
        
        # Mock config with MULTIPLE invalid objectives
        invalid_config = [
            {
                "slug": "bad-quest-1",
                "objectives_json": [{"id": "o1", "kind": "bad", "rule": {"a":1}}],
                "world_id": "w1", "track_id": "t1", "order_index": 1, "title": "T1", "short_description": "S1", "detailed_description": "D1", "rubric_id": "r1", "starting_code_path": "p1", "unlocks_boss_id": None, "unlocks_layout_id": None, "base_xp_reward": 10, "mastery_xp_bonus": 5
            },
            {
                "slug": "bad-quest-2",
                "objectives_json": [{"id": "o2", "kind": "exit_code", "rule": {}}], # Missing expected
                "world_id": "w1", "track_id": "t1", "order_index": 2, "title": "T2", "short_description": "S2", "detailed_description": "D2", "rubric_id": "r2", "starting_code_path": "p2", "unlocks_boss_id": None, "unlocks_layout_id": None, "base_xp_reward": 10, "mastery_xp_bonus": 5
            }
        ]
        
        with patch('arcade_app.seed_quests_standard_worlds.STANDARD_QUESTLINES', invalid_config):
            # Should raise ValueError with summary of errors
            with self.assertRaises(ValueError) as cm:
                seed_standard_world_quests(mock_db, validate_only=True)
            
            msg = str(cm.exception)
            self.assertIn("Validation Failed: 2 errors found", msg)
            # We can't easily check printed output without capturing stdout, but we know it raised.
            
            # Verify DB was NOT touched
            mock_db.add.assert_not_called()
            mock_db.commit.assert_not_called()

        # Mock DB
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.one_or_none.return_value = None
        
        # Mock config with VALID objective
        valid_config = [{
            "slug": "test-quest-valid",
            "world_id": "world-test",
            "track_id": "track-test",
            "order_index": 1,
            "title": "Test",
            "short_description": "Desc",
            "detailed_description": "Detailed",
            "rubric_id": "rubric",
            "starting_code_path": "path",
            "unlocks_boss_id": None,
            "unlocks_layout_id": None,
            "base_xp_reward": 10,
            "mastery_xp_bonus": 5,
            "objectives_json": [
                {
                    "id": "obj1",
                    "kind": "exit_code_zero",
                    "rule": {"kind": "exit_code_zero"}
                }
            ]
        }]
        
        with patch('arcade_app.seed_quests_standard_worlds.STANDARD_QUESTLINES', valid_config):
            seed_standard_world_quests(mock_db)
            # Should not raise
            pass

if __name__ == '__main__':
    unittest.main()
