from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import os
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = REPO_ROOT / "data" / "quests"

def load_questpack(path: Path) -> list[str]:
  raw = json.loads(path.read_text(encoding="utf-8"))

  # Support: list[{quest_path:"docs/quests/sql-ignition"}]
  if isinstance(raw, list):
    slugs: list[str] = []
    for item in raw:
      if isinstance(item, dict) and "quest_path" in item:
        slugs.append(Path(item["quest_path"]).name)
      elif isinstance(item, dict) and "slug" in item:
        slugs.append(str(item["slug"]))
    return slugs

  # Support future wrapper: { quests:[{slug:"..."}] }
  if isinstance(raw, dict) and "quests" in raw:
    out = []
    for q in raw["quests"]:
      out.append(str(q["slug"]))
    return out

  raise ValueError("Unsupported questpack format")


def run_pytest(quest_dir: Path) -> int:
  public_dir = quest_dir / "grading" / "public"
  if not public_dir.exists():
    print(f"[FAIL] missing grading/public for {quest_dir.name}")
    return 1

  cmd = [sys.executable, "-m", "pytest", "-q", str(public_dir)]
  
  # Inject REPO_ROOT into PYTHONPATH so "data._shared" imports work
  env = os.environ.copy()
  old_path = env.get("PYTHONPATH", "")
  env["PYTHONPATH"] = f"{REPO_ROOT}{os.pathsep}{old_path}"

  p = subprocess.run(cmd, cwd=str(quest_dir), env=env)
  return p.returncode


def swap_in_solution(quest_dir: Path) -> tuple[Path, bytes] | None:
  # Check for task.sql first
  ws = quest_dir / "workspace" / "task.sql"
  sol = quest_dir / "grading" / "solutions" / "task.sql"

  # Fallback to query.sql if task.sql not found (for legacy support if needed, but per spec we use task.sql)
  if not ws.exists() and (quest_dir / "workspace" / "query.sql").exists():
     ws = quest_dir / "workspace" / "query.sql"
  
  if not sol.exists() and (quest_dir / "grading" / "solutions" / "query.sql").exists():
     sol = quest_dir / "grading" / "solutions" / "query.sql"

  if not ws.exists():
    raise FileNotFoundError(f"missing workspace/task.sql for {quest_dir.name}")
  if not sol.exists():
    raise FileNotFoundError(f"missing grading/solutions/task.sql for {quest_dir.name}")

  original = ws.read_bytes()
  shutil.copy2(sol, ws)
  return (ws, original)

def restore_swap(swap: tuple[Path, bytes] | None) -> None:
  if not swap:
    return
  path, data = swap
  path.write_bytes(data)

def main(argv: list[str] | None = None) -> int:
  ap = argparse.ArgumentParser()
  ap.add_argument("--questpack", type=str, required=True)
  ap.add_argument("--mode", choices=["student", "solution"], default="student")
  ap.add_argument("--only-slug", type=str, default=None)
  args = ap.parse_args(argv)

  questpack_path = (REPO_ROOT / args.questpack).resolve() if not Path(args.questpack).is_absolute() else Path(args.questpack)
  slugs = load_questpack(questpack_path)

  if args.only_slug:
    slugs = [s for s in slugs if s == args.only_slug]
    if not slugs:
      print(f"No matching slug: {args.only_slug}")
      return 2

  failures: list[str] = []

  for slug in slugs:
    quest_dir = DATA_QUESTS / slug
    if not quest_dir.exists():
      print(f"[FAIL] missing quest dir: {quest_dir}")
      failures.append(slug)
      continue

    swap = None
    try:
      if args.mode == "solution":
        swap = swap_in_solution(quest_dir)

      rc = run_pytest(quest_dir)
      if rc == 0:
        print(f"[PASS] {slug}")
      else:
        print(f"[FAIL] {slug}")
        failures.append(slug)
    finally:
      restore_swap(swap)

  summary = {
    "total": len(slugs),
    "passed": len(slugs) - len(failures),
    "failed": len(failures),
    "errors": [],
    "slugs": []
  }
  
  # Re-construct status per slug for JSON?
  # Simplification: we know failures.
  for s in slugs:
      status = "failed" if s in failures else "passed"
      summary["slugs"].append({"slug": s, "status": status})

  print(f"EF_RUNNER_RESULT_JSON={json.dumps(summary)}")

  if failures:
    print("\nFailed quests:")
    for s in failures:
      print(f" - {s}")
    return 1
  
  print(f"\nEF_RUN_WORLD_SUMMARY: {summary['passed']}/{summary['total']} passed.")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
