import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.audit_codex_quality import check_quality_signals, is_stub

# Mock frontmatter
class MockPost:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = metadata

def test_quality_signals_perfect():
    """Test a file with all signals present."""
    with patch('frontmatter.load', return_value=MockPost(
        content="Here is an Example:\n```python\nprint(1)\n```\nSee also [foo](codex:foo).",
        metadata={"level": "beginner", "tags": ["python"], "related": ["codex:bar"]}
    )):
        signals = check_quality_signals(Path("dummy.md"))
        assert len(signals) == 0

def test_quality_signals_missing_all():
    """Test a file with all signals missing."""
    with patch('frontmatter.load', return_value=MockPost(
        content="Just text.",
        metadata={}
    )):
        signals = check_quality_signals(Path("dummy.md"))
        assert len(signals) == 4
        assert any("level" in s for s in signals)
        assert any("tags" in s for s in signals)
        assert any("examples" in s for s in signals)
        assert any("related" in s for s in signals)

def test_quality_signals_partial():
    """Test partial compliance."""
    with patch('frontmatter.load', return_value=MockPost(
        content="```python\ncode\n```",
        metadata={"level": "advanced"}
    )):
        signals = check_quality_signals(Path("dummy.md"))
        assert len(signals) == 2 # Missing tags, Missing related
        assert not any("level" in s for s in signals)
        assert not any("examples" in s for s in signals)
