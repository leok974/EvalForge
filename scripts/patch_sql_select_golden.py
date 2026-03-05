"""
scripts/patch_sql_select_golden.py

One-shot patch: makes sql-select the SQL golden exemplar.
  - Loads tutorial.md / briefing.md / lore.md / hints.md from disk
  - Sets key_terms wired to Codex slugs
  - Polishes objective display text (no validator changes)
  - Updates tiered_hints
  - Persists to DB
"""
import asyncio, json, sys, os
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

QUEST_DIR = Path("docs/quests/sql-select")
SLUG = "sql-select"

KEY_TERMS = [
    "select",
    "from",
    "where",
    "order-by",
    "limit",
]

TIERED_HINTS = {
    "concept": (
        "Write a minimal query first: `SELECT col FROM table;` "
        "then add WHERE / ORDER BY / LIMIT only if tests need them."
    ),
    "guided": (
        "Most failures are **shape** issues. Open **Query Inspector → Result** "
        "and compare column headers first, then row order. "
        "If order matters, add `ORDER BY some_column ASC;`."
    ),
    "full_solution": (
        "Add a deterministic ORDER BY. If there can be ties, use a tiebreaker: "
        "`ORDER BY primary_col ASC, id ASC;`. "
        "Then check that column names match exactly — aliases (`AS name`) help."
    ),
}

# Polished objective text — IDs and validators are NOT changed
OBJECTIVE_TEXT_MAP = {
    "sql_check":          "Query returns the expected rows and columns (exact output shape).",
    "fs_snapshot":        "Required workspace files are present.",
    "obj_sql_select_kwd": "Query uses a SELECT … FROM … statement.",
}


async def patch():
    tutorial_md  = (QUEST_DIR / "tutorial.md").read_text(encoding="utf-8")
    briefing_md  = (QUEST_DIR / "briefing.md").read_text(encoding="utf-8")
    lore_md      = (QUEST_DIR / "lore.md").read_text(encoding="utf-8")

    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as s:
        result = await s.execute(select(QuestDefinition).where(QuestDefinition.slug == SLUG))
        q = result.scalars().first()
        if not q:
            print(f"❌ Quest '{SLUG}' not found in DB")
            return

        # Content fields
        q.tutorial_md  = tutorial_md
        q.briefing_md  = briefing_md
        q.lore_md      = lore_md
        q.tiered_hints_json = TIERED_HINTS
        q.key_terms    = KEY_TERMS

        # Polish objective display text (safe — no validator changes)
        if q.objectives_json:
            patched_objs = []
            for obj in q.objectives_json:
                new_text = OBJECTIVE_TEXT_MAP.get(obj.get("id", ""))
                if new_text:
                    obj = {**obj, "text": new_text}
                patched_objs.append(obj)
            q.objectives_json = patched_objs

        s.add(q)
        await s.commit()

        print(f"✅ Patched quest '{SLUG}'")
        print(f"   tutorial_md  : {len(tutorial_md)} chars")
        print(f"   briefing_md  : {len(briefing_md)} chars")
        print(f"   lore_md      : {len(lore_md)} chars")
        print(f"   key_terms    : {KEY_TERMS}")
        print(f"   objectives   : {[o.get('id') for o in q.objectives_json]}")

asyncio.run(patch())
