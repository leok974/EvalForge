
import unittest
import sys
import os
import libcst as cst

sys.path.insert(0, os.path.abspath('.'))

from scripts.upgrade_objectives_state import StateObjectiveTransformer

class TestDriftChecks(unittest.TestCase):

    def test_drift_detected_in_seed_file(self):
        """Asserts that StateObjectiveTransformer detects missing objectives."""
        
        # 1. Mock Golden Map with a quest that needs objectives
        golden_map = {
            "quest_needs_update": {
                "type": "state",
                "files": ["foo.txt"], # Should trigger fs_snapshot
                "git": {"has_dot_git": False}
            }
        }
        
        # 2. Mock Source Code (Seed file)
        # A simple list def
        source_code = """
STANDARD_QUESTLINES = [
    {
        "slug": "quest_needs_update",
        "objectives_json": [
           {"id": "existing", "kind": "exit_code", "rule": {}}
        ]
    }
]
"""
        tree = cst.parse_module(source_code)
        
        # 3. specific test: Ensure transformer finds it
        transformer = StateObjectiveTransformer(golden_map)
        modified_tree = tree.visit(transformer)
        
        # 4. Assert
        self.assertGreater(transformer.modified_count, 0, "Drift not detected (transformer did not modify tree)")
        
        # verify fs_snapshot was added
        new_code = modified_tree.code
        self.assertIn("fs_snapshot", new_code)
        self.assertIn("must_exist", new_code)
        self.assertIn("foo.txt", new_code)

    def test_no_drift_when_up_to_date(self):
        """Asserts that StateObjectiveTransformer does nothing if objectives exist."""
        
        golden_map = {
            "quest_clean": {
                "type": "state",
                "files": ["foo.txt"],
                "git": {}
            }
        }
        
        # Seed already has fs_snapshot
        source_code = """
STANDARD_QUESTLINES = [
    {
        "slug": "quest_clean",
        "objectives_json": [
           {'id': 'fs_snapshot', 'kind': 'fs_snapshot', 'rule': {'must_exist': ['foo.txt']}}
        ]
    }
]
"""
        tree = cst.parse_module(source_code)
        
        transformer = StateObjectiveTransformer(golden_map)
        tree.visit(transformer)
        
        self.assertEqual(transformer.modified_count, 0, "Drift detected falsely (transformer modified tree)")

if __name__ == '__main__':
    unittest.main()
