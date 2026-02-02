"""
Tests for Codex reference resolver.
"""

import os
import pytest
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from codex_audit_missing import codex_ref_to_path, check_ref_exists


class TestCodexRefResolver:
    """Test reference resolution logic."""
    
    def test_path_format(self):
        """Test path format: glossary/python/interpreter"""
        result = codex_ref_to_path("glossary/python/interpreter")
        assert result == str(Path("data/codex/glossary/python/interpreter.md"))
    
    def test_path_format_with_codex_prefix(self):
        """Test path format with codex: prefix"""
        result = codex_ref_to_path("codex:glossary/python/print")
        assert result == str(Path("data/codex/glossary/python/print.md"))
    
    def test_flat_format(self):
        """Test flat format: glossary-python-string"""
        result = codex_ref_to_path("glossary-python-string")
        assert result == str(Path("data/codex/glossary-python-string.md"))
    
    def test_single_word_ref(self):
        """Test single word reference"""
        result = codex_ref_to_path("basics")
        assert result == str(Path("data/codex/basics.md"))
    
    def test_empty_ref(self):
        """Test empty reference returns None"""
        assert codex_ref_to_path("") is None
        assert codex_ref_to_path(None) is None
    
    def test_home_ref(self):
        """Test special 'home' reference returns None"""
        assert codex_ref_to_path("home") is None
        assert codex_ref_to_path("codex:home") is None
    
    def test_invalid_characters(self):
        """Test invalid characters return None"""
        assert codex_ref_to_path("glossary/python/../etc/passwd") is None
        assert codex_ref_to_path("glossary//double-slash") is not None  # Should still resolve
        assert codex_ref_to_path("glossary<script>") is None
    
    def test_nested_path(self):
        """Test deeply nested path"""
        result = codex_ref_to_path("concepts/advanced/python/async-await")
        assert result == str(Path("data/codex/concepts/advanced/python/async-await.md"))


class TestCheckRefExists:
    """Test file existence checking."""
    
    def test_existing_file(self):
        """Test checking an existing file (if any exist)"""
        # This will depend on what files exist
        # For now, just test the function doesn't crash
        exists, path = check_ref_exists("glossary/python/interpreter")
        assert isinstance(exists, bool)
        assert path is None or isinstance(path, str)
    
    def test_nonexistent_file(self):
        """Test checking a file that doesn't exist"""
        exists, path = check_ref_exists("glossary/nonexistent/term")
        assert exists is False
        assert path is not None  # Should still resolve to a path


class TestCodexRefNormalization:
    """Test reference normalization edge cases."""
    
    def test_multiple_slashes(self):
        """Test handling multiple consecutive slashes"""
        result = codex_ref_to_path("glossary//python//interpreter")
        # Should still produce a valid path (OS normalizes it)
        assert result is not None
        assert "interpreter.md" in result
    
    def test_trailing_slash(self):
        """Test handling trailing slashes"""
        result = codex_ref_to_path("glossary/python/")
        assert result is not None
    
    def test_mixed_separators(self):
        """Test different separator types"""
        # Hyphen in ID
        result1 = codex_ref_to_path("glossary/python/async-await")
        assert "async-await.md" in result1
        
        # Underscore in ID  
        result2 = codex_ref_to_path("glossary/python/async_await")
        assert "async_await.md" in result2
