"""
scripts/generate_debt_remaining.py
Generates docs/audits/DEBT_REMAINING_67.json — the canonical freeze of the
remaining debt quests after Phase Debt-1 pruning.

For each slug the JSON captures:
  - world
  - track
  - missing_fields: list of field names that are still absent
  - has_tests: bool (does a test file exist on disk or in grading_json?)
  - recommended_strategy: "tests_pass" | "ast" | "source_regex" | "state"
  - quest_folder: absolute path if found
"""
import sys, os, json, asyncio
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from scripts.utils_questpacks import get_all_quest_slugs

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

DOCS_DIR   = Path("data/quests")
DOCS_DIR2  = Path("docs/quests")
OUT_PATH   = Path("docs/audits/DEBT_REMAINING_67.json")

# World → preferred objective strategy
WORLD_STRATEGY = {
    "world-python":     "ast",
    "world-sql":        "tests_pass",
    "world-js":         "tests_pass",
    "world-typescript": "tests_pass",
    "world-react":      "tests_pass",
    "world-git":        "state",
    "world-infra":      "state",
    "world-docker":     "state",
    "world-agents":     "source_regex",
    "world-ml":         "tests_pass",
    "unknown":          "source_regex",
}

def _find_quest_folder(slug: str) -> str | None:
    for d in (DOCS_DIR / slug, DOCS_DIR2 / slug):
        if d.exists():
            return str(d)
    return None

def _has_tests(slug: str, folder: str | None, grading_json) -> bool:
    """True if there's a test file on disk or a grading_json with tests_pass config."""
    if grading_json and isinstance(grading_json, dict):
        if "tests_pass" in grading_json or "test_command" in grading_json:
            return True
    if folder:
        p = Path(folder)
        for pat in ("test_*.py", "*.test.js", "*.test.ts", "*.spec.ts", "*.spec.js"):
            if list(p.glob(pat)):
                return True
        if (p / "tests").exists():
            return True
    return False

async def generate():
    manifest_path = Path("data/seed/active_curriculum.json")
    active_slugs = set()
    if manifest_path.exists():
        with open(manifest_path) as f:
            active_slugs = set(json.load(f).get("active_slugs", []))

    referenced = get_all_quest_slugs()

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    records = []

    async with async_session() as session:
        quests = (await session.execute(select(QuestDefinition))).scalars().all()

        for q in quests:
            if q.slug in active_slugs:
                continue

            folder = _find_quest_folder(q.slug)
            if not folder:
                continue  # zombie — already pruned

            missing = []
            if not (q.briefing_md and q.briefing_md.strip()) and not (q.detailed_description and q.detailed_description.strip()):
                missing.append("briefing")
            if not (q.starter_code and q.starter_code.strip()) and not (
                q.workspace_json and "files" in q.workspace_json and
                any(f.get("content", "").strip() for f in q.workspace_json["files"])
            ):
                missing.append("workspace")
            if not (q.objectives_json and len(q.objectives_json) > 0):
                missing.append("objectives")
            is_t2 = "-t2-" in q.slug or "_t2_" in q.slug or "(T2)" in (q.title or "") or "Tier 2" in (q.title or "")
            if is_t2 and len(q.key_terms or []) < 3:
                missing.append("key_terms")

            # Check golden artifacts
            p = Path(folder)
            has_golden = (p / "golden.run.json").exists() or (p / "golden.state.json").exists()
            if not has_golden:
                missing.append("golden")

            records.append({
                "slug":                   q.slug,
                "world":                  q.world_id or "unknown",
                "track":                  q.track_id or "unknown",
                "title":                  q.title or "",
                "missing_fields":         missing,
                "missing_count":          len(missing),
                "has_tests":              _has_tests(q.slug, folder, q.grading_json),
                "recommended_strategy":   WORLD_STRATEGY.get(q.world_id or "unknown", "source_regex"),
                "is_referenced":          q.slug in referenced,
                "quest_folder":           folder,
            })

    # Sort: fewest missing fields first, then by world strategy priority
    strategy_order = ["tests_pass", "ast", "source_regex", "state"]
    records.sort(key=lambda r: (r["missing_count"], strategy_order.index(r["recommended_strategy"]) if r["recommended_strategy"] in strategy_order else 99))

    out = {
        "generated_at": "2026-02-25",
        "total": len(records),
        "quests": records
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"✅ Generated {OUT_PATH}: {len(records)} debt quests")

    # Print summary
    from collections import Counter
    by_world   = Counter(r["world"]   for r in records)
    by_missing = Counter(f for r in records for f in r["missing_fields"])
    by_strat   = Counter(r["recommended_strategy"] for r in records)

    print("\nBy World:")
    for w, c in by_world.most_common():
        print(f"  {w}: {c}")
    print("\nBy Missing Field:")
    for f, c in by_missing.most_common():
        print(f"  {f}: {c}")
    print("\nBy Recommended Strategy:")
    for s, c in by_strat.most_common():
        print(f"  {s}: {c}")

if __name__ == "__main__":
    asyncio.run(generate())
