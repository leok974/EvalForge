import asyncio
import os
import sys
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import models
sys.path.append(os.getcwd())
try:
    from arcade_app.models import QuestDefinition
except ImportError:
    print("Error: Could not import QuestDefinition. Run from project root.")
    sys.exit(1)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/arcade")

PLACEHOLDERS = ["term-1", "term-2", "term-3", "Example pending", "TODO:"]

def is_placeholder(text: str) -> bool:
    if not text:
        return False
    for p in PLACEHOLDERS:
        if p.lower() in text.lower():
            return True
    return False

async def audit_db():
    print(f"Connecting to {DATABASE_URL}...")
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    try:
        async with async_session() as session:
            stmt = select(QuestDefinition)
            result = await session.execute(stmt)
            quests = result.scalars().all()

            print(f"Auditing {len(quests)} quests...")
            issues_found = 0

            for q in quests:
                has_issues = False
                
                # Check key_terms (list of strings or dicts)
                if q.key_terms:
                    for term in q.key_terms:
                        term_str = term if isinstance(term, str) else term.get("term", "")
                        if is_placeholder(term_str):
                            print(f"[{q.slug}] Placeholder in key_terms: {term}")
                            has_issues = True

                # Check tiered_hints_json (values only)
                if q.tiered_hints_json:
                    for k, v in q.tiered_hints_json.items():
                        if is_placeholder(v):
                            print(f"[{q.slug}] Placeholder in tiered_hints[{k}]: {v}")
                            has_issues = True

                # Check codex_references (list of strings)
                if q.codex_references:
                    for ref in q.codex_references:
                        if is_placeholder(ref):
                            print(f"[{q.slug}] Placeholder in codex_references: {ref}")
                            has_issues = True

                if has_issues:
                    issues_found += 1

            if issues_found == 0:
                print("\n✅ No placeholders found in DB!")
            else:
                print(f"\n🚨 Found issues in {issues_found} quests.")

    except Exception as e:
        print(f"Error during audit: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(audit_db())
