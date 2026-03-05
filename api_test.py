import urllib.request
import json
from pprint import pprint

url = 'http://localhost:8092/api/quests/sql-t2-groupby-having/run'
data = json.dumps({
    "code": "SELECT category FROM products GROUP BY category -- HAVING COUNT(",
    "language": "sql",
    "mode": "tests",
    "idempotency_key": "test_run_sql_32"
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={
    'Content-Type': 'application/json',
    'x-dev-user': 'dev-user'
})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        res = json.loads(response.read().decode())
        print("Run passed:", res.get("passed"))
        print("Exit code:", res.get("exit_code"))
        artifacts = res.get("artifacts")
        if artifacts:
            print("Artifact keys:", artifacts.keys())
            if "sql_trace" in artifacts:
                print(f"Trace entries: {len(artifacts['sql_trace'])}")
            if "sql_student_result" in artifacts:
                 print("Included result table!")
        else:
            print("No artifacts found in response!")
            print(res)
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
