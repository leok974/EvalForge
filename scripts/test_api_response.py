#!/usr/bin/env python3
"""Test API call to python-ignition to see actual objective_results."""

import requests
import json

# Test with broken code
payload = {
    "code": "",
    "language": "python",
    "mode": "execute",
    "workspace": [
        {"path": "task.py", "content": "print('Hello')"}
    ]
}

print("🔍 Testing /api/quests/python-ignition/run")
print(f"Payload: {json.dumps(payload, indent=2)}\n")

response = requests.post(
    "http://localhost:8092/api/quests/python-ignition/run",
    json=payload,
    headers={"X-Dev-User": "test"}
)

print(f"Status: {response.status_code}")
print(f"\nResponse JSON:")
result = response.json()
print(json.dumps(result, indent=2))

print(f"\n{'='*60}")
print("OBJECTIVE_RESULTS:")
print(f"{'='*60}")
for obj in result.get('objective_results', []):
    print(f"\nID: {obj.get('id')}")
    print(f"  OK: {obj.get('ok')}")
    print(f"  Detail: {obj.get('detail')}")
    print(f"  Kind: {obj.get('kind')}")
    print(f"  Expected: {obj.get('expected')}")
    print(f"  Actual: {obj.get('actual')}")
    print(f"  Diff: {obj.get('diff')}")
