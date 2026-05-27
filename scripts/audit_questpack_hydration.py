#!/usr/bin/env python3
"""
audit_questpack_hydration.py -Questpack workspace-hydration integrity audit.

For every quest in every active questpack that defines workspace.entrypoint,
this script verifies that the corresponding workspace_json row in the DB:

  1. Has an "entrypoint" key whose value matches the questpack definition.
  2. Has a non-empty "files" list.
  3. Contains a file whose path equals the declared entrypoint.

Any mismatch means the quest was seeded without the entrypoint field (likely
from an older version of questpack_seed.py) and will break the live IDE
workspace resolver.

Exit codes:
  0  All audited quests pass.
  1  One or more quests fail the hydration check.
  2  DB connection failed -no DB checks run; source failures still exit 1.

Usage:
  python scripts/audit_questpack_hydration.py
  python scripts/audit_questpack_hydration.py --pack data/questpacks/docker_ignition.json
  python scripts/audit_questpack_hydration.py --verbose
"""

import json
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).parent.parent
ACTIVE_PACKS_FILE = ROOT / "configs" / "questpacks_active.json"

# ── Args ───────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Audit questpack workspace hydration in DB")
parser.add_argument("--pack", help="Audit a single questpack file instead of all active packs")
parser.add_argument("--verbose", "-v", action="store_true", help="Print every quest result")
args = parser.parse_args()

# ── Pack list ─────────────────────────────────────────────────────────────────

def load_active_packs() -> list[str]:
    if not ACTIVE_PACKS_FILE.exists():
        print(f"[AUDIT] ERROR: {ACTIVE_PACKS_FILE} not found.", file=sys.stderr)
        sys.exit(2)
    data = json.loads(ACTIVE_PACKS_FILE.read_text(encoding="utf-8"))
    return data.get("active_questpacks", [])

pack_paths = [args.pack] if args.pack else load_active_packs()


# ── Quest parsing (handles all 3 questpack shapes) ────────────────────────────

def iter_quests(pack_data) -> list[dict]:
    """
    Questpacks come in three shapes:
      1. Top-level list of quest dicts / strings
      2. Top-level dict with "quests" key → list
      3. Top-level dict with "entries" key → list
    Returns only dict-form quest entries (string slugs have no workspace def).
    """
    raw: list = []
    if isinstance(pack_data, list):
        raw = pack_data
    elif isinstance(pack_data, dict):
        raw = pack_data.get("quests") or pack_data.get("entries") or []
    return [q for q in raw if isinstance(q, dict)]


@dataclass
class QuestSpec:
    slug: str
    pack_file: str
    expected_entrypoint: str
    source_ws_dir: Path | None = field(default=None)


def resolve_files_from(files_from: str, pack_path: Path) -> Path | None:
    if not files_from:
        return None
    resolved = (pack_path.parent / files_from).resolve()
    return resolved if resolved.exists() else None


# ── Collect specs ─────────────────────────────────────────────────────────────

specs: list[QuestSpec] = []

for rel_path in pack_paths:
    pack_path = ROOT / rel_path
    if not pack_path.exists():
        print(f"[AUDIT] WARN: questpack not found: {rel_path}")
        continue
    try:
        pack_data = json.loads(pack_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[AUDIT] WARN: parse error in {pack_path.name}: {e}")
        continue

    for q in iter_quests(pack_data):
        slug = q.get("slug") or q.get("id")
        if not slug:
            continue
        ws = q.get("workspace")
        if not isinstance(ws, dict):
            continue
        entrypoint = ws.get("entrypoint")
        if not entrypoint:
            continue  # workspace block present but no entrypoint declared -not our problem

        ws_dir = resolve_files_from(ws.get("files_from", ""), pack_path)
        specs.append(QuestSpec(
            slug=slug,
            pack_file=pack_path.name,
            expected_entrypoint=entrypoint,
            source_ws_dir=ws_dir,
        ))

print(f"[AUDIT] {len(specs)} quests with declared workspace.entrypoint across {len(pack_paths)} pack(s).")

if not specs:
    print("[AUDIT] Nothing to audit. Exiting.")
    sys.exit(0)


# ── SOURCE CHECK: entrypoint file must exist on disk ─────────────────────────

source_failures: list[str] = []

for spec in specs:
    if spec.source_ws_dir is None:
        if args.verbose:
            print(f"  [SOURCE SKIP] {spec.slug}: files_from dir not found, cannot check disk")
        continue
    ep_path = spec.source_ws_dir / spec.expected_entrypoint
    if not ep_path.exists():
        print(
            f"  [SOURCE FAIL] {spec.slug}: {spec.expected_entrypoint!r} missing on disk\n"
            f"                Expected: {ep_path}\n"
            f"                Pack:     {spec.pack_file}"
        )
        source_failures.append(spec.slug)
    elif args.verbose:
        print(f"  [SOURCE OK]   {spec.slug}: {spec.expected_entrypoint} [ok]")


# ── DB CHECK: workspace_json must have entrypoint + files ────────────────────

DB_URL = (
    os.environ.get("DATABASE_URL", "postgresql://evalforge:evalforge@localhost:5435/evalforge")
    .replace("postgresql+asyncpg", "postgresql")
    .replace("postgresql+psycopg2", "postgresql")
)

db_ok = False
db_rows: dict[str, dict] = {}  # slug → workspace_json

try:
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("DATABASE_URL", DB_URL)
    from sqlmodel import create_engine, Session, select, col
    from arcade_app.models import QuestDefinition

    engine = create_engine(DB_URL, echo=False)
    slugs_to_check = [s.slug for s in specs]

    with Session(engine) as session:
        results = session.exec(
            select(QuestDefinition).where(
                col(QuestDefinition.slug).in_(slugs_to_check)
            )
        ).all()
        for row in results:
            wj = row.workspace_json
            db_rows[row.slug] = wj if isinstance(wj, dict) else {}

    db_ok = True
    print(f"[AUDIT] DB connected. {len(db_rows)}/{len(slugs_to_check)} quests found in DB.")

except Exception as e:
    print(f"[AUDIT] WARN: DB unavailable ({type(e).__name__}: {e})", file=sys.stderr)
    print(f"[AUDIT] Skipping DB checks. Re-run with DB accessible for full audit.", file=sys.stderr)


db_failures: list[str] = []
not_in_db: list[str] = []

if db_ok:
    for spec in specs:
        if spec.slug not in db_rows:
            not_in_db.append(spec.slug)
            if args.verbose:
                print(f"  [NOT IN DB]   {spec.slug} -not seeded yet")
            continue

        wj = db_rows[spec.slug]
        ep_db = wj.get("entrypoint")
        files_db = wj.get("files") or []
        fail_reasons = []

        # 1. entrypoint key must exist and match
        if not ep_db:
            fail_reasons.append(
                f"workspace_json missing 'entrypoint' key "
                f"(re-seed with updated questpack_seed.py)"
            )
        elif ep_db != spec.expected_entrypoint:
            fail_reasons.append(
                f"entrypoint mismatch: DB={ep_db!r}, questpack={spec.expected_entrypoint!r}"
            )

        # 2. files list must not be empty
        if not files_db:
            fail_reasons.append("workspace_json.files is empty (workspace dir missing or not seeded)")

        # 3. entrypoint file must be in the files list
        if files_db:
            paths_in_db = {f.get("path") for f in files_db if isinstance(f, dict)}
            if spec.expected_entrypoint not in paths_in_db:
                fail_reasons.append(
                    f"entrypoint {spec.expected_entrypoint!r} not in workspace_json.files "
                    f"(present: {sorted(paths_in_db)})"
                )

        if fail_reasons:
            print(f"  [DB FAIL]     {spec.slug} ({spec.pack_file}):")
            for r in fail_reasons:
                print(f"                  → {r}")
            db_failures.append(spec.slug)
        elif args.verbose:
            print(
                f"  [DB OK]       {spec.slug}: entrypoint={ep_db!r}, "
                f"{len(files_db)} file(s) [ok]"
            )

    if not_in_db:
        label = "quests not yet in DB" if len(not_in_db) > 1 else "quest not yet in DB"
        print(
            f"[AUDIT] {len(not_in_db)} {label} (not a failure -run questpack_seed.py to seed):"
        )
        if args.verbose:
            for s in not_in_db:
                print(f"  {s}")


# ── Summary ───────────────────────────────────────────────────────────────────

all_failures = source_failures + db_failures
total = len(specs)

print()
if not all_failures and not source_failures:
    db_status = "DB + source" if db_ok else "source only (no DB)"
    print(f"[AUDIT] PASS: {total} quests checked, 0 failures ({db_status}).")
    sys.exit(0)
else:
    print(f"[AUDIT] FAIL: {len(all_failures)} failure(s) across {total} quests.")
    if source_failures:
        print(f"  Source ({len(source_failures)}): {source_failures}")
    if db_failures:
        print(f"  DB     ({len(db_failures)}): {db_failures}")

    # Dedupe affected packs for the fix hint
    failed_slugs = set(all_failures)
    packs_to_reseed = sorted({s.pack_file for s in specs if s.slug in failed_slugs})
    print()
    print("Fix: re-seed the affected pack(s) using the updated questpack_seed.py:")
    for p in packs_to_reseed:
        print(f"  docker compose exec backend bash -c \\")
        print(f"    \"cd /app && PYTHONPATH=/app python scripts/questpack_seed.py data/questpacks/{p}\"")
    sys.exit(1)
