import asyncio
import os
import json
from arcade_app.services.code_runner import run_code
from arcade_app.schemas.quest_run import RunRequest

async def main():
    os.environ["EXECUTION_ENABLED"] = "1"
    os.environ["EXECUTION_DOCKER_IMAGE_SQL"] = "python:3.11-slim" # Or whatever EvalForge uses
    sql = """
    SELECT name, city
    FROM users
    ORDER BY name ASC;
    """
    
    workspace = [{"path": "task.sql", "content": sql}]
    
    # Just to get the exact payload from the runner
    result = await run_code(
        code=sql,
        language="sql",
        mode="run",
        quest_slug="sql-select",
        workspace=workspace
    )
    
    print("--- Artifacts Result ---")
    if result.artifacts:
        print("sql_student_result:", json.dumps(result.artifacts.get("sql_student_result"), indent=2))
        print("sql_trace length:", len(result.artifacts.get("sql_trace", [])))
    else:
        print("ARTIFACTS NONE")
        
if __name__ == "__main__":
    asyncio.run(main())
