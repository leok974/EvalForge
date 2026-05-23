#!/usr/bin/env python3
"""
scripts/run_docker_questpack.py

Grade-by-inspection runner for world-docker questpacks.

Docker quests (Dockerfile / compose.yaml) have no subprocess to run.
The submitted source IS the artifact.  All grading is done by static
objective validators (source_regex, yaml_structure) operating on the
raw file content.  This runner reads the workspace entrypoint file,
passes it as `code` to validate_quest_attempt, and reports results.

Usage:
  python scripts/run_docker_questpack.py --questpack data/questpacks/docker_ignition.json --mode student
  python scripts/run_docker_questpack.py --questpack data/questpacks/docker_ignition.json --mode solution
"""

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).parent.parent))

# Force UTF-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    from arcade_app.services.quest_validate import validate_quest_attempt
except ImportError:
    print("Error: Could not import arcade_app.services.quest_validate.")
    print("Ensure you are running from the repo root or have PYTHONPATH set.")
    sys.exit(1)


@dataclass
class QuestResult:
    slug: str
    passed: bool
    details: List[Dict[str, Any]]
    code: str


# Default entrypoint per quest — overridden by quest-level "entrypoint" field.
_DEFAULT_ENTRYPOINTS = {
    "compose.yaml": "compose.yaml",
    "docker-compose.yml": "docker-compose.yml",
}
_DOCKERFILE_DEFAULT = "Dockerfile"


def _get_entrypoint(quest_def: Dict[str, Any]) -> str:
    """Return the primary file name to read as source code."""
    ws = quest_def.get("workspace") or {}
    ep = ws.get("entrypoint") or quest_def.get("entrypoint")
    if ep:
        return ep
    # Infer from files list
    files = ws.get("files") or []
    names = [f.get("path", "") for f in files if isinstance(f, dict)]
    for n in names:
        if "compose" in n.lower() or n.endswith(".yaml") or n.endswith(".yml"):
            return n
    # Default to Dockerfile
    return _DOCKERFILE_DEFAULT


class _MockQuest:
    """Minimal shim so validate_quest_attempt can read objectives."""

    def __init__(self, quest_def: Dict[str, Any], language: str = "docker"):
        objectives_raw = (
            quest_def.get("objectives_json")
            or quest_def.get("objectives")
            or []
        )
        # Normalize rule_json -> rule
        self.objectives_json = []
        for o in objectives_raw:
            o_copy = o.copy()
            if "rule_json" in o_copy and "rule" not in o_copy:
                o_copy["rule"] = o_copy["rule_json"]
            self.objectives_json.append(o_copy)

        self.runtime_rules_json = quest_def.get("runtime_rules_json", {})
        self.tier = quest_def.get("tier", 1)
        self.language = language


def run_quest(
    quest_def: Dict[str, Any],
    questpack_path: Path,
    mode: str = "student",
) -> QuestResult:
    slug = quest_def["slug"]
    print(f"  Running {slug} [{mode}]...")

    # --- Resolve workspace directory ---
    ws_conf = quest_def.get("workspace") or {}
    files_from = ws_conf.get("files_from")

    if files_from:
        ws_dir = (questpack_path.parent / files_from).resolve()
    else:
        # Canonical layout: data/quests/<slug>/workspace
        ws_dir = (questpack_path.parent.parent / "quests" / slug / "workspace").resolve()

    if not ws_dir.exists():
        print(f"    ERROR: workspace not found: {ws_dir}")
        return QuestResult(slug, False, [{"id": "config", "ok": False, "detail": f"Workspace not found: {ws_dir}"}], "")

    # --- Choose entrypoint ---
    entrypoint = _get_entrypoint(quest_def)

    # --- Swap in solution for solution mode ---
    if mode == "solution":
        sol_dir = ws_dir.parent / "grading" / "solutions"
        if sol_dir.exists():
            sol_file = sol_dir / entrypoint
            if sol_file.exists():
                code = sol_file.read_text(encoding="utf-8")
                print(f"    (solution) reading {sol_file}")
            else:
                # Try first file in solutions dir
                sol_files = list(sol_dir.iterdir())
                if sol_files:
                    code = sol_files[0].read_text(encoding="utf-8")
                    print(f"    (solution) reading {sol_files[0]}")
                else:
                    print(f"    WARN: solution dir empty, falling back to workspace")
                    code = (ws_dir / entrypoint).read_text(encoding="utf-8") if (ws_dir / entrypoint).exists() else ""
        else:
            print(f"    WARN: no grading/solutions dir, falling back to workspace")
            code = (ws_dir / entrypoint).read_text(encoding="utf-8") if (ws_dir / entrypoint).exists() else ""
    else:
        code_file = ws_dir / entrypoint
        if not code_file.exists():
            print(f"    ERROR: entrypoint not found: {code_file}")
            return QuestResult(slug, False, [{"id": "config", "ok": False, "detail": f"Entrypoint not found: {code_file}"}], "")
        code = code_file.read_text(encoding="utf-8")

    # --- Validate ---
    lang = quest_def.get("language", "docker")
    mock_quest = _MockQuest(quest_def, language=lang)

    try:
        results = validate_quest_attempt(
            code=code,
            stdout="",
            stderr="",
            exit_code=0,
            timed_out=False,
            quest_def=mock_quest,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return QuestResult(slug, False, [{"id": "validator_crash", "ok": False, "detail": str(e)}], code)

    passed = all(r["ok"] for r in results)

    if passed:
        print(f"    PASS")
    else:
        print(f"    FAIL")
        for r in results:
            status = "OK" if r["ok"] else "FAIL"
            print(f"      [{r['id']}] {status}: {r.get('detail', '')}")

    return QuestResult(slug, passed, results, code)


def main():
    parser = argparse.ArgumentParser(description="Run Docker Questpack (grade-by-inspection)")
    parser.add_argument("--questpack", required=True, help="Path to questpack JSON")
    parser.add_argument("--only-slug", help="Run only specific quest slug")
    parser.add_argument("--mode", choices=["student", "solution"], default="student")
    args = parser.parse_args()

    qp_path = Path(args.questpack)
    if not qp_path.exists():
        print(f"Questpack not found: {qp_path}")
        sys.exit(1)

    with open(qp_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    quests: List[Dict[str, Any]] = []
    if isinstance(data, list):
        quests = data
    elif isinstance(data, dict):
        quests = data.get("quests") or data.get("packs") or []

    if args.only_slug:
        quests = [q for q in quests if q.get("slug") == args.only_slug]

    print(f"=== Docker Questpack: {qp_path.name} | {len(quests)} quest(s) | mode={args.mode} ===")

    total = len(quests)
    passed_count = 0
    failed_count = 0
    slug_results = []

    for q in quests:
        slug = q.get("slug")
        if not slug:
            continue
        result = run_quest(q, qp_path, mode=args.mode)
        slug_results.append({"slug": slug, "status": "passed" if result.passed else "failed"})
        if result.passed:
            passed_count += 1
        else:
            failed_count += 1

    summary = {
        "total": total,
        "passed": passed_count,
        "failed": failed_count,
        "errors": [],
        "slugs": slug_results,
    }
    print(f"\nEF_RUNNER_RESULT_JSON={json.dumps(summary)}")

    if failed_count > 0:
        print(f"\nFAIL: {passed_count}/{total} passed")
        sys.exit(1)
    else:
        print(f"\nPASS: {passed_count}/{total} passed")


if __name__ == "__main__":
    main()
