from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PACK = ROOT / "data" / "questpacks" / "agents_core.json"
DATA_QUESTS = ROOT / "data" / "quests"

def slug_from_quest_path(p: str) -> str:
    p = p.replace("\\", "/").rstrip("/")
    return p.split("/")[-1]

def copy_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def main() -> int:
    if not PACK.exists():
        raise SystemExit(f"missing: {PACK}")

    pack = json.loads(PACK.read_text(encoding="utf-8"))
    if not isinstance(pack, list):
        raise SystemExit("agents_core.json must be a top-level array of {quest_path}")

    hydrated = 0
    for item in pack:
        if not isinstance(item, dict) or "quest_path" not in item:
            continue
        quest_path = item["quest_path"]
        if not isinstance(quest_path, str):
            continue

        slug = slug_from_quest_path(quest_path)
        docs_dir = ROOT / quest_path
        if not docs_dir.exists():
            print(f"[SKIP] docs missing: {docs_dir}")
            continue

        data_dir = DATA_QUESTS / slug
        workspace_dir = data_dir / "workspace"
        sol_dir = data_dir / "grading" / "solutions"
        pub_dir = data_dir / "grading" / "public"

        # Ensure dirs
        pub_dir.mkdir(parents=True, exist_ok=True)
        # Ensure solution dir parent exists (grading)
        (data_dir / "grading").mkdir(parents=True, exist_ok=True)

        # Map docs structure → execution structure
        # docs: starter/  -> data: workspace/
        # docs: solution/ -> data: grading/solutions/
        copy_dir(docs_dir / "starter", workspace_dir)
        copy_dir(docs_dir / "solution", sol_dir)

        # Optional: copy fixtures if present (some worlds use fixtures/)
        if (docs_dir / "fixtures").exists():
            copy_dir(docs_dir / "fixtures", data_dir / "fixtures")

        hydrated += 1
        print(f"[OK] hydrated {slug}")

    print(f"[DONE] hydrated {hydrated} quests into data/quests/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
