import pytest
import requests
import json
import time

BASE_URL = "http://localhost:19010"

def test_session_persistence():
    # 1. Get Active Session (Initial)
    print("\n1. Fetching Active Session...")
    resp = requests.get(f"{BASE_URL}/api/session/active")
    assert resp.status_code == 200
    session = resp.json()
    sid = session["id"]
    print(f"   Session ID: {sid}")
    print(f"   Initial State: {session['world_id']} / {session['track_id']} / {session['mode']}")
    
    # 2. Simulate Stream Request (Change Context)
    print("\n2. Sending Stream Request (Changing Context)...")
    new_context = {
        "world_id": "world-js",
        "track_id": "react-frontend",
        "mode": "explain",
        "message": "Hello Persistence"
    }
    
    stream_url = f"{BASE_URL}/apps/arcade_app/users/leo/sessions/{sid}/query/stream"
    
    # We just need to trigger the request, we don't care about the full stream output for this test
    # But we need to consume it to ensure the backend processes it fully (especially the 'done' part where assistant msg is saved)
    with requests.post(stream_url, json=new_context, stream=True) as r:
        assert r.status_code == 200
        for line in r.iter_lines():
            pass # Consume stream
            
    # Allow a tiny bit of time for async DB writes if any (though await should handle it)
    time.sleep(1)
    
    # 3. Get Active Session (Verify Update)
    print("\n3. Verifying Persistence...")
    resp = requests.get(f"{BASE_URL}/api/session/active")
    updated_session = resp.json()
    
    print(f"   Updated State: {updated_session['world_id']} / {updated_session['track_id']} / {updated_session['mode']}")
    
    assert updated_session["world_id"] == "world-js"
    assert updated_session["track_id"] == "react-frontend"
    assert updated_session["mode"] == "explain"
    
    # 4. Verify History
    print("\n4. Verifying Chat History...")
    history = updated_session["history"]
    print(f"   History Length: {len(history)}")
    
    # Should have at least User message and Assistant message
    assert len(history) >= 2
    assert history[-2]["role"] == "user"
    assert history[-2]["content"] == "Hello Persistence"
    assert history[-1]["role"] == "assistant"
    
    print("✅ Persistence Verified!")

if __name__ == "__main__":
    test_session_persistence()
