import requests
import json

payload = {
    "code": "message = 'wrong'",
    "language": "python",
    "mode": "validate"
}

response = requests.post(
    "http://localhost:8092/api/quests/hello-variable/run",
    json=payload,
    headers={"X-Dev-User": "test"}
)

print("Status:", response.status_code)
print("\nObjective Results:")
result = response.json()
for obj in result.get('objective_results', []):
    print(f"\n  ID: {obj.get('id')}")
    print(f"  OK: {obj.get('ok')}")
    print(f"  Detail: {obj.get('detail')}")
    print(f"  Kind: {obj.get('kind')}")
    print(f"  Expected: {obj.get('expected')}")
    print(f"  Actual: {obj.get('actual')}")
    print(f"  Diff: {obj.get('diff')}")
