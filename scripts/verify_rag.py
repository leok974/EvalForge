import requests
import json
import sys

def verify_rag():
    url = "http://localhost:19010/apps/arcade_app/users/leo/sessions/sess_verify/query/stream"
    payload = {
        "message": "How do I handle state in LangGraph?",
        "mode": "explain",
        "world_id": "world-agents",
        "track_id": "world-agents" 
    }
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}

    print(f"Connecting to {url}...")
    try:
        with requests.post(url, json=payload, headers=headers, stream=True) as r:
            print(f"Status Code: {r.status_code}")
            for line in r.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        data_str = decoded[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            # Some data might be JSON, some might be plain text depending on event type
                            # But looking at agent.py, most data is just string or JSON string
                            print(f"RECEIVED: {data_str}")
                        except:
                            pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_rag()
