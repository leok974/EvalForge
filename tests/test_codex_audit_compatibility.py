
import unittest
import sys
import os

# Add scripts directory to path to import the module under test
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import the specific function we want to test
from codex_audit_missing import extract_codex_refs

class TestCodexAuditCompatibility(unittest.TestCase):
    def test_dict_format_tier1_standard(self):
        """Test the new Tier-1 friendly dict format."""
        quest_data = {
            "key_terms": {
                "key_terms": ["term1", "term2"],
                "codex_references": ["codex:glossary/test/term1", "codex:glossary/test/term2"]
            },
            "tutorial_md": "Some content"
        }
        
        refs = extract_codex_refs(quest_data)
        self.assertIn("codex:glossary/test/term1", refs)
        self.assertIn("codex:glossary/test/term2", refs)
        self.assertEqual(len(refs), 2)

    def test_list_format_legacy(self):
        """Test the legacy list format."""
        quest_data = {
            "key_terms": [
                {
                    "term": "term1",
                    "codex_ref": "codex:glossary/test/term1"
                },
                {
                    "term": "term2",
                    "codex_ref": "codex:glossary/test/term2"
                }
            ],
            "tutorial_md": "Some content"
        }
        
        refs = extract_codex_refs(quest_data)
        self.assertIn("codex:glossary/test/term1", refs)
        self.assertIn("codex:glossary/test/term2", refs)
        self.assertEqual(len(refs), 2)

    def test_mixed_invalid_input(self):
        """Test that invalid or empty inputs don't crash."""
        # Empty dict
        refs = extract_codex_refs({})
        self.assertEqual(len(refs), 0)
        
        # Empty key_terms
        refs = extract_codex_refs({"key_terms": []})
        self.assertEqual(len(refs), 0)
        
        # Missing codex_ref in list mode
        quest_data = {
            "key_terms": [
                {"term": "term1"} # No codex_ref
            ]
        }
        refs = extract_codex_refs(quest_data)
        self.assertEqual(len(refs), 0)

    def test_top_level_codex_references(self):
        """Test that top-level codex_references are always extracted."""
        quest_data = {
            "codex_references": ["codex:glossary/global/ref"]
        }
        refs = extract_codex_refs(quest_data)
        self.assertIn("codex:glossary/global/ref", refs)

if __name__ == '__main__':
    unittest.main()
