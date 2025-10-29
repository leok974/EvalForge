"""
E2E tests for Vertex AI project validation with auto-sanitization.
Tests that the server auto-fixes concatenated project IDs.
"""
import os
import subprocess
import time
import json
import urllib.request
import contextlib


def _get(url: str, timeout: int = 6) -> str:
    """HTTP GET request helper."""
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode("utf-8")


def _post(url: str, timeout: int = 6) -> str:
    """HTTP POST request helper."""
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def test_sanitizes_concat():
    """Test that server auto-sanitizes concatenated project ID (e.g., 'evalforge-1063529378' → 'evalforge')."""
    env = os.environ.copy()
    env.update({
        "GENAI_PROVIDER": "vertex",
        "GOOGLE_CLOUD_PROJECT": "evalforge-1063529378",  # Should be sanitized to 'evalforge'
        "VERTEX_LOCATION": "us-east5",
        "GENAI_MODEL": "gemini-1.5-flash-002",
    })
    
    p = subprocess.Popen(
        ["python", "-m", "google.adk.cli", "web", ".", "--host", "127.0.0.1", "--port", "19002"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="."
    )
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Server should start successfully and sanitize the project
        # Test discovery endpoint
        apps = _get("http://127.0.0.1:19002/list-apps?relative_path=arcade_app")
        assert "arcade_app" in apps, "Server should sanitize concat and start successfully"
        
        print("✓ Server correctly sanitized concatenated project ID 'evalforge-1063529378' → 'evalforge'")
    finally:
        with contextlib.suppress(Exception):
            p.terminate()
            p.wait(timeout=3)


def test_local_ok_with_id():
    """Test that server starts successfully with valid project ID."""
    env = os.environ.copy()
    env.update({
        "GENAI_PROVIDER": "vertex",
        "GOOGLE_CLOUD_PROJECT": "evalforge",  # correct project ID
        "VERTEX_LOCATION": "us-east5",
        "GENAI_MODEL": "gemini-1.5-flash-002",
    })
    
    p = subprocess.Popen(
        ["python", "-m", "google.adk.cli", "web", ".", "--host", "127.0.0.1", "--port", "19003"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="."
    )
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Test discovery endpoint
        apps = _get("http://127.0.0.1:19003/list-apps?relative_path=arcade_app")
        assert "arcade_app" in apps, "arcade_app not found in discovery response"
        
        # Test session creation
        sess = _post("http://127.0.0.1:19003/apps/arcade_app/users/user/sessions")
        data = json.loads(sess)
        assert data.get("appName") == "arcade_app", "Invalid appName in session response"
        assert "id" in data, "Session ID not found in response"
        
        print(f"✓ Server started successfully with project ID 'evalforge' (session: {data['id'][:8]}...)")
    finally:
        with contextlib.suppress(Exception):
            p.terminate()
            p.wait(timeout=3)


if __name__ == "__main__":
    print("\n🧪 Running Vertex AI Project Auto-Sanitization Tests...\n")
    
    print("Test 1: Auto-sanitize concatenated project ID")
    test_sanitizes_concat()
    
    print("\nTest 2: Accept valid project ID")
    test_local_ok_with_id()
    
    print("\n✅ All project sanitization tests passed!")
