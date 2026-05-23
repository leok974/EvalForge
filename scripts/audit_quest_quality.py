import asyncio
import os
import sys
import json
from sqlmodel import select
from pathlib import Path

# Add CWD to sys.path to find arcade_app
sys.path.insert(0, os.getcwd())

from arcade_app.database import engine
from arcade_app.models import QuestDefinition, TrackDefinition, KnowledgeChunk
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from arcade_app.services.quest_visibility import get_active_quest_config

async def audit_world(world_id: str):
    print(f"Auditing World: {world_id}")
    print("=" * 70)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    active_slugs, _ = get_active_quest_config()
    
    async with async_session() as session:
        # Load tracks for cross-ref
        track_stmt = select(TrackDefinition.id).where(TrackDefinition.world_id == world_id)
        valid_track_ids = set((await session.execute(track_stmt)).scalars().all())

        stmt = select(QuestDefinition).where(QuestDefinition.world_id == world_id)
        results = await session.execute(stmt)
        quests = results.scalars().all()
        
        if not quests:
            print(f"❌ No quests found for world {world_id}")
            return False
            
        all_passed = True
        
        for q in quests:
            errors = []
            
            # --- 1. Content Completeness ---
            if not q.briefing_md or len(q.briefing_md.strip()) < 10:
                errors.append("Missing or too-short Briefing")
            
            if not q.tutorial_md or len(q.tutorial_md.strip()) < 10:
                errors.append("Missing or too-short Tutorial")
            
            if not q.lore_md or len(q.lore_md.strip()) < 10:
                errors.append("Missing or too-short Lore")

            # --- 2. Hints (Modern format check) ---
            hints = q.tiered_hints_json or {}
            source = hints.get("markdown_source")
            if not source or len(str(source)) < 10:
                errors.append("Missing modern hints (markdown_source)")
            elif not str(source).startswith("# "):
                errors.append("Malformed hints: Missing top-level # Title header (required for frontend parser)")
            
            if hints.get("hints") and isinstance(hints.get("hints"), list):
                # This looks like the old format
                errors.append("Legacy hints format detected (list in 'hints' key)")

            # --- 3. Workspace Integrity ---
            ws = q.workspace_json or {}
            files = ws.get("files", [])
            paths = [f['path'].replace("\\", "/") for f in files]
            
            if not files:
                errors.append("Empty workspace (no files)")
            else:
                if q.language == "sql":
                    if "task.sql" not in paths: errors.append("Missing task.sql")
                    if "example.sql" not in paths: errors.append("Missing example.sql")
                elif q.language == "python":
                    if "task.py" not in paths and "main.py" not in paths: errors.append("Missing task.py/main.py")

            # --- 4. Infrastructure Metadata ---
            if not q.objectives_json or len(q.objectives_json) == 0:
                errors.append("Empty objectives_json (required for Success Criteria tab)")

            if q.language == "sql" and q.db_engine == "postgres":
                 if not q.featured_tables:
                      errors.append("Postgres quest missing featured_tables")
                 if not q.db_explorer_enabled:
                      errors.append("Postgres quest has db_explorer_enabled = False")
                 if q.db_explorer_mode != "quest_scoped":
                      errors.append(f"Postgres quest should use db_explorer_mode = 'quest_scoped' (current: {q.db_explorer_mode})")
                 if not q.key_terms or len(q.key_terms) < 2:
                      errors.append("Postgres relational quest should have at least 2 key terms")
            
            if q.starting_code_path:
                if q.language == "sql" and not q.starting_code_path.endswith(".sql"):
                     errors.append(f"SQL quest has non-SQL starting_code_path: {q.starting_code_path}")
            
            # --- 5. Structural Attachment ---
            if q.track_id not in valid_track_ids:
                 errors.append(f"Quest attached to non-existent track: {q.track_id}")
            
            if q.slug not in active_slugs:
                 errors.append(f"Quest NOT in active curriculum (not in configs/questpacks_active.json)")

            if q.codex_references:
                for ref in q.codex_references:
                    # Strip prefix for DB lookup
                    db_ref = ref.replace("codex:", "")
                    kb_stmt = select(KnowledgeChunk).where(KnowledgeChunk.source_id == db_ref)
                    kb_res = await session.execute(kb_stmt)
                    if not kb_res.first():
                         errors.append(f"Codex reference NOT found in DB: {ref} (searched for {db_ref})")

            # --- 7. Database Content Integrity (Postgres Specific) ---
            if q.db_engine == "postgres" and q.db_explorer_enabled and q.featured_tables:
                for table in q.featured_tables:
                    try:
                        # Safety identifier check
                        if not table.isidentifier():
                            errors.append(f"Featured table '{table}' has invalid name")
                            continue
                        count_stmt = text(f"SELECT COUNT(*) FROM public.{table}")
                        count_res = await session.execute(count_stmt)
                        count = count_res.scalar()
                        if count == 0:
                            errors.append(f"Featured table '{table}' is EMPTY in public schema. Preview will be blank.")
                    except Exception as e:
                        errors.append(f"Featured table '{table}' existence/data check failed: {str(e)}")

            if errors:
                all_passed = False
                print(f"❌ [{q.slug}] {q.title}")
                for err in errors:
                    print(f"   - {err}")
            else:
                print(f"✅ [{q.slug}] {q.title} is complete.")
                
        return all_passed

if __name__ == "__main__":
    world = sys.argv[1] if len(sys.argv) > 1 else "sql_tier3"
    success = asyncio.run(audit_world(world))
    if not success:
        sys.exit(1)
        print("\nWorld Audit Passed!")
