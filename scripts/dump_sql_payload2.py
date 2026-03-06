import asyncio
import os
import json
from arcade_app.services.code_runner import run_code

def main():
    os.environ["EXECUTION_ENABLED"] = "1"
    os.environ["EXECUTION_DOCKER_IMAGE_SQL"] = "python:3.12-slim"
    sql = "SELECT name, city FROM users ORDER BY name ASC;"
    
    workspace = {
        "files": [
            {"path": "task.sql", "content": sql},
            {"path": "fixtures/schema.sql", "content": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT);"},
            {"path": "fixtures/seed.sql", "content": "INSERT INTO users (name, city) VALUES ('Alice', 'Paris'), ('Bob', 'Tokyo');"}
        ]
    }
    
    try:
        result = run_code(
            language="sql",
            code=sql,
            mode="run",
            quest_slug="sql-select",
            workspace=workspace
        )
        print(f"OK: {result.ok}")
        print(f"EXIT CODE: {result.exit_code}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        print("ARTIFACTS:")
        if result.artifacts:
            print(json.dumps(result.artifacts, indent=2))
        else:
            print("NONE")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    main()
