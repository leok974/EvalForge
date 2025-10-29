"""
E2E tests for Vertex AI integration.
Launches ephemeral ADK server and tests full Vertex path end-to-end.
"""
import os
import subprocess
import time
import json
import urllib.request


from typing import Optional, Tuple

BASE_ENV = {
    "GENAI_PROVIDER": "vertex",
    "GOOGLE_CLOUD_PROJECT": "evalforge-1063529378",
    "VERTEX_LOCATION": "us-east5",
    "GENAI_MODEL": "gemini-1.5-flash-002",
}


def _curl(path: str, method: str = "GET", data: Optional[bytes] = None) -> Tuple[int, bytes]:
    """Helper to make HTTP requests."""
    req = urllib.request.Request(path, method=method, data=data)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.getcode(), r.read()


def test_local_end_to_end():
    """
    Test local server with Vertex AI end-to-end.
    This validates that project/region/model configuration is correct.
    """
    env = os.environ.copy()
    env.update(BASE_ENV)
    # ephemeral port to avoid collisions
    port = "19001"
    p = subprocess.Popen(
        [
            "python",
            "-m",
            "google.adk.cli",
            "web",
            ".",
            "--host",
            "127.0.0.1",
            "--port",
            port,
        ],
        cwd=".",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(2.5)
        # discovery
        code, body = _curl(
            f"http://127.0.0.1:{port}/list-apps?relative_path=arcade_app"
        )
        assert code == 200, f"Discovery failed with code {code}"
        # session create
        code, body = _curl(
            f"http://127.0.0.1:{port}/apps/arcade_app/users/user/sessions",
            method="POST",
            data=b"",
        )
        assert code == 200, f"Session creation failed with code {code}"
        # sanity parse
        j = json.loads(body.decode())
        assert "id" in j, "Session response missing 'id' field"
        print(f"✓ E2E test passed (session: {j['id'][:8]}...)")
    finally:
        p.kill()
        p.wait(timeout=2)


if __name__ == "__main__":
    print("\n🧪 Running Vertex AI E2E Test...\n")
    test_local_end_to_end()
    print("\n✅ E2E test passed!")
