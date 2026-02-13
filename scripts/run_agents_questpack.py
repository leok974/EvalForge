from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = ROOT / "data" / "quests"

def slug_from_quest_path(p: str) -> str:
  p = p.replace("\\", "/").rstrip("/")
  return p.split("/")[-1]

def load_slugs(pack_path: Path) -> List[str]:
  obj = json.loads(pack_path.read_text(encoding="utf-8"))
  slugs: List[str] = []
  if isinstance(obj, list):
    for it in obj:
      if isinstance(it, dict) and isinstance(it.get("quest_path"), str):
        slugs.append(slug_from_quest_path(it["quest_path"]))
      elif isinstance(it, dict) and isinstance(it.get("slug"), str):
        slugs.append(it["slug"])
      elif isinstance(it, str):
        slugs.append(it)
  elif isinstance(obj, dict) and isinstance(obj.get("quests"), list):
    for it in obj["quests"]:
      if isinstance(it, dict) and isinstance(it.get("slug"), str):
        slugs.append(it["slug"])
      elif isinstance(it, dict) and isinstance(it.get("quest_path"), str):
        slugs.append(slug_from_quest_path(it["quest_path"]))
  return slugs

def swap_in_solutions(quest_dir: Path) -> List[Tuple[Path, Path]]:
  """Copy grading/solutions/** into workspace/**. Return list of (dst, backup) to restore later."""
  sol = quest_dir / "grading" / "solutions"
  ws = quest_dir / "workspace"
  backups: List[Tuple[Path, Path]] = []
  if not sol.exists():
    return backups

  for src in sol.rglob("*.py"):
    rel = src.relative_to(sol)
    dst = ws / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
      bak = dst.with_suffix(dst.suffix + ".bak")
      shutil.copy2(dst, bak)
      backups.append((dst, bak))
    else:
      backups.append((dst, Path()))  # Path() sentinel = no backup
    shutil.copy2(src, dst)
  return backups

def restore(backups: List[Tuple[Path, Path]]) -> None:
  for dst, bak in backups:
    try:
      if bak and bak.exists():
        shutil.copy2(bak, dst)
        bak.unlink()
      else:
        if dst.exists():
          dst.unlink()
    except Exception:
      pass

def run_pytest(quest_dir: Path) -> int:
  pub = quest_dir / "grading" / "public"
  if not pub.exists():
    return 1
  cmd = [sys_python(), "-m", "pytest", "-q", str(pub)]
  env = os.environ.copy()
  env.setdefault("PYTHONUTF8", "1")
  res = subprocess.run(cmd, cwd=str(quest_dir), env=env)
  return int(res.returncode)

def sys_python() -> str:
  # prefer PYTHON_BIN if user sets it
  return os.environ.get("PYTHON_BIN") or os.environ.get("PYTHON") or "python"

def main() -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("--questpack", type=str, required=True)
  ap.add_argument("--mode", choices=["student", "solution"], default="student")
  ap.add_argument("--only-slug", type=str, default="")
  args = ap.parse_args()

  pack_path = (ROOT / args.questpack).resolve() if not Path(args.questpack).is_absolute() else Path(args.questpack)
  slugs = load_slugs(pack_path)
  if args.only_slug:
    slugs = [s for s in slugs if s == args.only_slug]

  if not slugs:
    print("EF_RUN_AGENTS_NO_SLUGS")
    return 2

  total = 0
  passed = 0

  for slug in slugs:
    quest_dir = DATA_QUESTS / slug
    if not quest_dir.exists():
      print(f"[MISS] {slug}: no data/quests folder")
      total += 1
      continue

    backups: List[Tuple[Path, Path]] = []
    try:
      if args.mode == "solution":
        backups = swap_in_solutions(quest_dir)
      rc = run_pytest(quest_dir)
      total += 1
      if rc == 0:
        passed += 1
        print(f"[PASS] {slug}")
      else:
        print(f"[FAIL] {slug}")
    finally:
      if backups:
        restore(backups)

  print(f"EF_RUN_AGENTS_SUMMARY: {passed}/{total} passing")
  return 0 if passed == total else 1

if __name__ == "__main__":
  raise SystemExit(main())
