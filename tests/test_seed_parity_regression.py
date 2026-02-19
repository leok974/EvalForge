
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from scripts.audit_seed_parity import audit_seed_parity

class TestSeedParityRegression(unittest.TestCase):

    @patch("scripts.audit_seed_parity.STANDARD_QUESTLINES", [{"slug": "seeded_quest"}])
    @patch("scripts.audit_seed_parity.get_all_quest_slugs", return_value={"seeded_quest"})
    @patch("scripts.audit_seed_parity.Path")
    def test_parity_pass(self, MockPath, mock_get_slugs):
        """Asserts audit passes when everything exists."""
        
        # Mock Path.exists() to always return True
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        MockPath.return_value = mock_path_instance
        
        # Capture stdout/exit
        with self.assertRaises(SystemExit) as cm:
             audit_seed_parity()
        
        self.assertEqual(cm.exception.code, 0)

    @patch("scripts.audit_seed_parity.STANDARD_QUESTLINES", [{"slug": "missing_workspace"}])
    @patch("scripts.audit_seed_parity.get_all_quest_slugs", return_value=set())
    @patch("scripts.audit_seed_parity.Path")
    def test_parity_fails_missing_workspace(self, MockPath, mock_get_slugs):
        """Asserts audit fails when seeded quest has no workspace."""
        
        # Mock Path.exists() to return False
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        MockPath.return_value = mock_path_instance
        
        # Capture stdout
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            with self.assertRaises(SystemExit) as cm:
                 audit_seed_parity()
            
            self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
