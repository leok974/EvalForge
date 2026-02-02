"""
Phase 9.1: Codex API Tests
Tests for secure Codex reference resolution and markdown retrieval.
"""
import pytest
from fastapi.testclient import TestClient
from arcade_app.main import app

client = TestClient(app)


class TestCodexAPI:
    """Test Codex API endpoint security and functionality."""
    
    def test_valid_ref_returns_markdown(self):
        """Valid codex reference returns markdown content."""
        # This assumes python/print.md exists from golden tutorial
        response = client.get("/api/codex?ref=codex:glossary/python/print")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "ref" in data
        assert data["ref"] == "codex:glossary/python/print"
        assert "title" in data
        assert "md" in data
        assert "path" in data
        
        # Markdown should contain heading
        assert "#" in data["md"]
        assert "print()" in data["md"] or "print" in data["title"].lower()
    
    def test_invalid_prefix_rejected(self):
        """Reference without 'codex:' prefix is rejected."""
        response = client.get("/api/codex?ref=glossary/python/print")
        
        assert response.status_code == 400
        assert "must start with 'codex:'" in response.json()["detail"]
    
    def test_path_traversal_rejected(self):
        """Path traversal attempts are rejected."""
        # Test various traversal patterns
        traversal_refs = [
            "codex:glossary/../../../etc/passwd",
            "codex:glossary/python/../../secrets",
            "codex:../secrets",
            "codex:glossary/python/../../../main.py"
        ]
        
        for ref in traversal_refs:
            response = client.get(f"/api/codex?ref={ref}")
            assert response.status_code == 400
            assert "path traversal" in response.json()["detail"].lower() or "invalid" in response.json()["detail"].lower()
    
    def test_backslash_rejected(self):
        """Backslashes in path are rejected."""
        response = client.get("/api/codex?ref=codex:glossary\\python\\print")
        
        assert response.status_code == 400
    
    def test_double_slash_rejected(self):
        """Double slashes are rejected."""
        response = client.get("/api/codex?ref=codex:glossary//python/print")
        
        assert response.status_code == 400
        assert "double slashes" in response.json()["detail"]
    
    def test_invalid_root_rejected(self):
        """References to invalid root directories are rejected."""
        # Only glossary, concepts, patterns allowed
        response = client.get("/api/codex?ref=codex:secrets/password")
        
        assert response.status_code == 400
        assert "root must be one of" in response.json()["detail"]
    
    def test_missing_file_returns_404(self):
        """Missing codex entry returns 404."""
        response = client.get("/api/codex?ref=codex:glossary/python/does-not-exist")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unsafe_characters_rejected(self):
        """Unsafe characters in path are rejected."""
        unsafe_refs = [
            "codex:glossary/python/print;rm -rf",
            "codex:glossary/python/print|cat",
            "codex:glossary/python/print\x00",
            "codex:glossary/PYTHON/PRINT",  # Uppercase not allowed
        ]
        
        for ref in unsafe_refs:
            try:
                response = client.get(f"/api/codex?ref={ref}")
            except Exception:
                # Client might reject malformed URL locally
                continue
            assert response.status_code == 400
    
    def test_title_extraction(self):
        """Title is extracted from H1 or falls back to filename."""
        response = client.get("/api/codex?ref=codex:glossary/python/print")
        
        if response.status_code == 200:
            data = response.json()
            # Should have some title (either from H1 or filename)
            assert data["title"]
            assert len(data["title"]) > 0
    
    def test_multiple_valid_refs(self):
        """Multiple valid references work correctly."""
        refs = [
            "codex:glossary/python/interpreter",
            "codex:glossary/python/syntax-error",
            "codex:glossary/python/string",
            "codex:glossary/python/indentation"
        ]
        
        for ref in refs:
            response = client.get(f"/api/codex?ref={ref}")
            # Should either return 200 (file exists) or 404 (doesn't exist yet)
            # But should NOT return 400 (these are valid ref formats)
            assert response.status_code in [200, 404]
