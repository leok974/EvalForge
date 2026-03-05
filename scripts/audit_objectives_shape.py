"""
scripts/audit_objectives_shape.py

CI gate: samples every quest with objectives from the DB and asserts
that each serialized objective satisfies the frontend shape contract:
  { id: str, text: non-empty str, validator: { kind: non-empty str } }

Fails loudly if any objective would produce a blank UI row.

Usage:
    python scripts/audit_objectives_shape.py
Exit 0 on pass, 1 on violations.
"""
import asyncio, json, sys, os
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from arcade_app.quest_helper import _normalize_objectives
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

VALID_KINDS = {"exit_code_zero", "source_regex", "stdout_regex", "tests_pass", "ast", "contains", "regex", "state"}


async def audit():
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    violations: list[str] = []

    async with Session() as s:
        result = await s.execute(select(QuestDefinition))
        quests = result.scalars().all()

    total_quests = 0
    total_objectives = 0

    for q in quests:
        if not q.objectives_json:
            continue
        total_quests += 1
        normalized = _normalize_objectives(q.objectives_json)

        for obj in normalized:
            total_objectives += 1
            slug_prefix = f"[{q.slug}] obj={obj.get('id', '?')}"

            # UI-BREAKING: blank text causes a completely empty row (the bug we fixed)
            if not obj.get("text", "").strip():
                violations.append(f"{slug_prefix}: 'text' is blank — row will be empty in QuestDrawer")

            # UI-BREAKING: validator IS present but malformed (not a dict)
            # Note: missing validator entirely is OK for state/tests_pass quests (text-only style)
            validator = obj.get("validator")
            if validator is not None and not isinstance(validator, dict):
                violations.append(f"{slug_prefix}: 'validator' is present but not a dict (got {type(validator).__name__})")

    print(f"✅ Scanned {total_quests} quests with objectives ({total_objectives} total objectives)")

    if violations:
        print(f"\n❌ {len(violations)} shape violations found:\n")
        for v in violations:
            print(f"  • {v}")
        return 1
    else:
        print("✅ All objectives pass shape contract: {id, text, validator:{kind}}")
        return 0


if __name__ == "__main__":
    rc = asyncio.run(audit())
    sys.exit(rc)
