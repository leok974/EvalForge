import requests
import json
import sys

def debug_stream():
    url = "http://localhost:8082/apps/arcade_app/users/test/sessions/sess_debug/query/stream_v2"
    payload = {"message": "start"}
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}

    print(f"Connecting to {url}...")
    try:
        with requests.post(url, json=payload, headers=headers, stream=True) as r:
            print(f"Status Code: {r.status_code}")
            print("--- Stream Start ---")
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    # Print raw bytes representation to see newlines/CRs
                    print(f"CHUNK: {repr(chunk)}")
                    # Also print decoded
                    try:
                        print(f"DECODED: {chunk.decode('utf-8')}")
                    except:
                        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_stream()
