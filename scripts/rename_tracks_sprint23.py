"""
Sprint 23: Rename track IDs in questpack JSONs to canonical <world>-<tier> convention.

Rename map (old → new):
  python-fundamentals        → python-foundry
  foundry-senior-systems     → python-systems
  fundamentals               → python-foundry   (alias, 1 quest)
  boss-prep                  → python-boss
  core-python                → python-ignition
  js-ignition                → js-foundry
  js-arrays                  → js-foundry
  js-objects                 → js-foundry
  js-functions               → js-foundry
  js-async                   → js-foundry
  js-errors                  → js-foundry
  js-modules                 → js-foundry
  ts-fundamentals            → ts-foundry
  git-fundamentals           → git-foundry
  track-sql (pack-level)     → sql-foundry
  track-html (pack-level)    → web-html
  track-css (pack-level)     → web-css
  track-docker-ignition      → docker-ignition
  track-docker-systems       → docker-systems
  python-selenium            → (no change)

Run: python scripts/rename_tracks_sprint23.py [--dry-run]
"""

import argparse
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).parent.parent

# Per-quest track_id renames (for quests that store track_id inside each quest object)
PER_QUEST_RENAMES = {
    "python-fundamentals": "python-foundry",
    "foundry-senior-systems": "python-systems",
    "fundamentals": "python-foundry",
    "boss-prep": "python-boss",
    "core-python": "python-ignition",
    "js-ignition": "js-foundry",
    "js-arrays": "js-foundry",
    "js-objects": "js-foundry",
    "js-functions": "js-foundry",
    "js-async": "js-foundry",
    "js-errors": "js-foundry",
    "js-modules": "js-foundry",
    "ts-fundamentals": "ts-foundry",
    "git-fundamentals": "git-foundry",
}

# Pack-level track_id renames (for packs that store track_id at the top level)
PACK_LEVEL_RENAMES = {
    "track-sql": "sql-foundry",
    "track-html": "web-html",
    "track-css": "web-css",
    "track-docker-ignition": "docker-ignition",
    "track-docker-systems": "docker-systems",
}

ACTIVE_QUESTPACKS = [
    "data/questpacks/python_systems.json",
    "data/questpacks/_tier2/python_tier2.json",
    "data/questpacks/foundry_python.json",
    "data/questpacks/python_selenium.json",
    "data/questpacks/web_html_core.json",
    "data/questpacks/web_css_core.json",
    "data/questpacks/sql_core.json",
    "data/questpacks/javascript_core.json",
    "data/questpacks/typescript_core.json",
    "data/questpacks/git_core.json",
    "data/questpacks/docker_ignition.json",
    "data/questpacks/docker_systems.json",
]


def process_pack(pack_path: pathlib.Path, dry_run: bool) -> list[str]:
    """Process one pack. Returns list of change descriptions."""
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    changes = []

    is_list = isinstance(data, list)
    quests = data if is_list else data.get("quests", [])

    # Pack-level rename
    if not is_list:
        old_tid = data.get("track_id")
        if old_tid and old_tid in PACK_LEVEL_RENAMES:
            new_tid = PACK_LEVEL_RENAMES[old_tid]
            changes.append(f"  pack-level track_id: {old_tid!r} → {new_tid!r}")
            if not dry_run:
                data["track_id"] = new_tid

    # Per-quest renames
    for q in quests:
        old_tid = q.get("track_id")
        if old_tid and old_tid in PER_QUEST_RENAMES:
            new_tid = PER_QUEST_RENAMES[old_tid]
            changes.append(f"  quest {q.get('slug', '?')!r}: track_id {old_tid!r} → {new_tid!r}")
            if not dry_run:
                q["track_id"] = new_tid

    if changes and not dry_run:
        pack_path.write_text(
            json.dumps(data, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN — no files will be modified\n")

    total = 0
    for rel in ACTIVE_QUESTPACKS:
        p = BASE / rel
        if not p.exists():
            print(f"SKIP: {rel}")
            continue
        changes = process_pack(p, args.dry_run)
        status = "DRY" if args.dry_run else "WROTE"
        if changes:
            print(f"[{status}] {p.name}:")
            for c in changes:
                print(c)
            total += len(changes)
        else:
            print(f"[OK]  {p.name}: no renames needed")

    print(f"\nTotal changes: {total}")


if __name__ == "__main__":
    sys.exit(main())
