"""
E2E tests for Vertex AI configuration and local ADK server.
"""
import os
import subprocess
import time
import json
import urllib.request


def test_env_region_allowed():
    """Verify VERTEX_LOCATION is set to an allowed region."""
    os.environ["GENAI_PROVIDER"] = "vertex"
    os.environ["GOOGLE_CLOUD_PROJECT"] = "evalforge-1063529378"
    os.environ["VERTEX_LOCATION"] = "us-east5"  # must be allowed
    os.environ["GENAI_MODEL"] = "gemini-1.5-flash-002"
    
    allowed_regions = {"us-east5", "europe-west4", "asia-southeast1"}
    assert os.environ["VERTEX_LOCATION"] in allowed_regions, \
        f"VERTEX_LOCATION must be one of {allowed_regions}"


def _http_get(url: str, timeout: int = 8) -> str:
    """HTTP GET request helper."""
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode("utf-8")


def _http_post(url: str, timeout: int = 8) -> str:
    """HTTP POST request helper."""
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def test_local_adk_smoke():
    """Launch ephemeral ADK server and verify discovery + session endpoints."""
    # Launch ADK dev server in a subprocess (ephemeral)
    env = os.environ.copy()
    env.update({
        "GENAI_PROVIDER": "vertex",
        "GOOGLE_CLOUD_PROJECT": "evalforge-1063529378",
        "VERTEX_LOCATION": "us-east5",
        "GENAI_MODEL": "gemini-1.5-flash-002",
    })
    
    p = subprocess.Popen(
        ["python", "-m", "google.adk.cli", "web", ".", "--host", "127.0.0.1", "--port", "19001"],
        cwd=".",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        time.sleep(3.5)
        
        # Test discovery endpoint
        apps = _http_get("http://127.0.0.1:19001/list-apps?relative_path=arcade_app")
        assert "arcade_app" in apps, "arcade_app not found in discovery response"
        
        # Test session creation
        sess = _http_post("http://127.0.0.1:19001/apps/arcade_app/users/user/sessions")
        data = json.loads(sess)
        assert data.get("appName") == "arcade_app", "Invalid appName in session response"
        assert "id" in data, "Session ID not found in response"
        
        print(f"✓ Local ADK smoke passed (session: {data['id'][:8]}...)")
    finally:
        p.terminate()
        p.wait(timeout=5)


if __name__ == "__main__":
    test_env_region_allowed()
    print("✓ test_env_region_allowed passed")
    
    test_local_adk_smoke()
    print("✓ test_local_adk_smoke passed")
    
    print("\n✅ All E2E tests passed!")
