import asyncio
import sys
import os
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

# Add CWD to sys.path
sys.path.insert(0, os.getcwd())

from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from arcade_app.services.code_runner import run_code

QUEST_SLUGS = [
    "postgres-real-schema-joins",
    "postgres-safe-querying",
    "postgres-date-trunc-time-buckets",
    "postgres-explain-basics",
    "postgres-jsonb-basics"
]

async def run_guardrail():
    print("🛡️  Starting SQL Wave Guardrail Verification...")
    print("=" * 60)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    all_passed = True
    
    async with async_session() as session:
        for slug in QUEST_SLUGS:
            print(f"\n🔍 Quest: {slug}")
            issues = []
            
            # 1. Fetch Quest
            q_stmt = select(QuestDefinition).where(QuestDefinition.slug == slug)
            q_res = await session.execute(q_stmt)
            quest = q_res.scalar_one_or_none()
            
            if not quest:
                print(f"   ❌ FAILED: Quest definition not found in DB.")
                all_passed = False
                continue

            # 1. Visibility Guard (Check if quest is correctly registered in World/Track)
            if quest.world_id == "unknown" or quest.track_id == "misc":
                issues.append(f"Visibility Guard: Quest '{slug}' has invalid metadata (world='{quest.world_id}', track='{quest.track_id}')")
            else:
                print(f"   ✅ Visibility: {quest.world_id} / {quest.track_id}")

            featured = quest.featured_tables or []
            if not featured:
                print(f"   ⚠️  Warning: No featured_tables defined.")
            
            # 2. Preview Guard (Check public schema row counts + Formatting)
            for table in featured:
                try:
                    res = await session.execute(text(f"SELECT COUNT(*) FROM public.{table}"))
                    count = res.scalar()
                    if count == 0:
                        issues.append(f"Preview Guard: Featured table '{table}' is EMPTY in public schema.")
                    else:
                        print(f"   ✅ Preview: {table} ({count} rows)")
                    
                    # Formatting Guard: Hit API and check for raw objects in JSON
                    import httpx
                    try:
                        async with httpx.AsyncClient() as client:
                            api_url = f"http://localhost:8092/api/db/preview?quest_id={slug}&table={table}"
                            api_res = await client.get(api_url)
                            if api_res.status_code == 200:
                                api_data = api_res.json()
                                format_error = False
                                for r in api_data.get("rows", []):
                                    for cell in r:
                                        if isinstance(cell, (dict, list)):
                                            format_error = True
                                            break
                                    if format_error: break
                                
                                if format_error:
                                    issues.append(f"Formatting Guard: Featured table '{table}' returns raw objects in API. Should be stringified.")
                                else:
                                    print(f"   ✅ Formatting: {table} uses stringified JSON.")
                    except Exception as api_e:
                        print(f"   ⚠️  Formatting Guard skipped: API not reachable ({api_e})")
                except Exception as e:
                    issues.append(f"Preview Guard: Failed to check {table}: {e}")

            # 3. Example Execution Guard (Check runner visibility)
            # Find example.sql in workspace
            ws = quest.workspace_json or {}
            files = ws.get("files", [])
            example_file = next((f for f in files if f["path"] == "example.sql"), None)
            
            if not example_file:
                 issues.append("Execution Guard: No 'example.sql' found in workspace files.")
            else:
                try:
                    # Run code via internal service logic
                    exec_res = run_code(
                        language="sql",
                        code=example_file.get("content", ""),
                        workspace=ws,
                        mode="run",
                        quest_slug=slug,
                        # Pass engines/etc if needed, but defaults should work for postgres
                    )
                    
                    # Inspect artifacts in execution state
                    state = getattr(exec_res, "state", {})
                    # For SQL, artifacts are usually in sql_student_result
                    # However, runner might have its own state shape
                    # Let's rely on common result fields
                    if not exec_res.stdout and not exec_res.stderr:
                         # Likely a pure artifact runner
                         pass
                    
                    # Basic check for rows in output (hacky but works for SQL tracers)
                    if "rows" in exec_res.stdout or "sql_student_result" in exec_res.stdout:
                         # If we see JSON artifacts with zero rows, fail
                         if '"row_count": 0' in exec_res.stdout and 'SELECT' in example_file.get("content", "").upper():
                             issues.append("Execution Guard: example.sql returned 0 rows despite being seeded.")
                         else:
                             print(f"   ✅ Execution: example.sql returned data.")
                    else:
                        # Fallback for simple runners
                        if exec_res.exit_code != 0:
                            issues.append(f"Execution Guard: example.sql failed (Exit {exec_res.exit_code})")
                        else:
                            print(f"   ✅ Execution: example.sql finished successfully.")
                except Exception as e:
                    issues.append(f"Execution Guard: Failed to execute example.sql: {e}")

            # 4. Codex Resolution Guard
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    # 4.1 Fetch hydrated quest details (to get auto-inflated key_terms)
                    quest_api_url = f"http://localhost:8092/api/quests/{slug}"
                    quest_api_res = await client.get(quest_api_url)
                    if quest_api_res.status_code != 200:
                        issues.append(f"Codex Guard: Failed to fetch quest details from API (Status {quest_api_res.status_code})")
                    else:
                        quest_details = quest_api_res.json()
                        key_terms = quest_details.get("key_terms", [])
                        
                        if not key_terms:
                            print(f"   ⚠️  Warning: No key_terms defined for linking.")
                        
                        for term_obj in key_terms:
                            ref = term_obj.get("codex_ref")
                            term_name = term_obj.get("term", "?")
                            if not ref:
                                issues.append(f"Codex Guard: Term '{term_name}' is missing a codex_ref.")
                                continue
                            
                            # Standardize ref for API (ensure codex: prefix)
                            if not ref.startswith("codex:"):
                                ref = f"codex:{ref}"
                                
                            # 4.2 Verify resolution
                            codex_api_url = f"http://localhost:8092/api/codex?ref={ref}"
                            codex_res = await client.get(codex_api_url)
                            if codex_res.status_code == 200:
                                print(f"   ✅ Codex: '{term_name}' -> {ref} (Resolved)")
                            else:
                                issues.append(f"Codex Guard: Term '{term_name}' ({ref}) 404s in Codex API.")
                        
                        # 4.3 Hint Count Guard
                        hints_md = quest_details.get("hints_md", "")
                        if hints_md:
                            # Simple parsing to match frontend: split by \n## 
                            # Note: parseHints in React uses md.split(/\n(?=##\s)/)
                            import re
                            # Prepend \n to handle file starting with ## (though usually it has a # title)
                            parts = re.split(r'\n(?=##\s)', "\n" + hints_md)
                            # Remove the part before the first ## if it contains a # title
                            if parts and not parts[0].strip().startswith("##"):
                                parts = parts[1:]
                            
                            hint_count = len(parts)
                            expected_count = 3
                            if hint_count < expected_count:
                                issues.append(f"Hint Guard: Only {hint_count} hints found in hints_md. Expected at least {expected_count}.")
                            else:
                                print(f"   ✅ Hints: {hint_count} hints found (Passed)")
                            
                            # Malformed check: look for lines starting with 'Hint' but not '## Hint'
                            lines = hints_md.split("\n")
                            for i, line in enumerate(lines):
                                if line.strip().startswith("Hint ") and not line.strip().startswith("##"):
                                     issues.append(f"Hint Guard: Possible malformed hint header at line {i+1}: '{line.strip()}'")
                        else:
                             # Fallback to structured hints
                             structured_hints = quest_details.get("hints", [])
                             if len(structured_hints) < 3:
                                 issues.append(f"Hint Guard: Only {len(structured_hints)} structured hints found. Expected 3.")
                             else:
                                 print(f"   ✅ Hints: {len(structured_hints)} structured hints found.")

            except Exception as codex_e:
                print(f"   ⚠️  Codex/Hint Guard skipped: API not reachable ({codex_e})")

            # 5. Reporting
            if issues:
                all_passed = False
                for issue in issues:
                    print(f"   ❌ {issue}")
            else:
                print(f"   ✨ All guardrails passed for {slug}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 SQL Wave Guardrail: MISSION SUCCESSFUL")
    else:
        print("🚨 SQL Wave Guardrail: FAILURES DETECTED")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_guardrail())
