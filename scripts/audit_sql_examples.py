import asyncio
import json
import os
import sys

# Ensure we can import from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlmodel import select
from arcade_app.services.code_runner import run_code

async def audit_examples():
    print("🚀 Starting SQL Example Result Audit...")
    print("=" * 60)
    
    any_failed = False
    
    async with engine.connect() as conn:
        stmt = select(QuestDefinition).where(QuestDefinition.db_engine == 'postgres')
        result = await conn.execute(stmt)
        quests = result.all()

        for q in quests:
            slug = q.slug
            example_path = os.path.join("data", "quests", slug, "workspace", "example.sql")
            if not os.path.exists(example_path):
                # Optionally warn or fail if required
                print(f"[SKIP] {slug}: Missing example.sql")
                continue

            with open(example_path, "r", encoding="utf-8") as f:
                code = f.read()

            # We need a workspace with fixtures to run the example
            # The code_runner.run_code with mode='run' handles quest fixtures
            # if we pass quest_slug.
            
            print(f"[CHECK] {slug}...")
            try:
                r = run_code("sql", code, mode="run", quest_slug=slug)
                
                # The result is in r.artifacts
                artifacts = getattr(r, "artifacts", {})
                student_result = artifacts.get("sql_student_result", {})
                row_count = student_result.get("row_count", 0)
                
                if row_count == 0:
                    print(f"  ❌ FAIL: returned 0 rows.")
                    any_failed = True
                else:
                    print(f"  ✅ PASS: {row_count} rows returned.")
            except Exception as e:
                print(f"  ❌ ERROR: {e}")
                any_failed = True

    print("=" * 60)
    if any_failed:
        print("❌ SQL Audit FAILED: Some examples returned 0 rows or errored.")
        sys.exit(1)
    else:
        print("✅ SQL Audit PASSED: All examples returned meaningful data.")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(audit_examples())
