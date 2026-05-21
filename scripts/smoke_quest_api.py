#!/usr/bin/env python3
"""
scripts/smoke_quest_api.py

Full learner path smoke test -- calls the live API for each active quest
and verifies that:
  - Solution code  -> passed=True  (all objectives green)
  - Starter code   -> passed=False (>=1 objective red)   [Python quests only]

Usage:
  python scripts/smoke_quest_api.py [--base-url http://localhost:8092] [--packs python|sql|js|selenium|all]
"""

import argparse
import json
import sys
import uuid
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).parent.parent
BASE_URL = "http://localhost:8092"
DEV_USER = "smoketest"


def post_run(slug, code, language, mode="validate"):
    url = f"{BASE_URL}/api/quests/{slug}/run"
    payload = json.dumps({
        "code": code,
        "language": language,
        "mode": mode,
        "idempotency_key": str(uuid.uuid4()),
    }).encode()
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json", "X-Dev-User": DEV_USER},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def find_solution(slug, language):
    quest_root = ROOT / "data" / "quests" / slug
    sol_dir = quest_root / "grading" / "solutions"
    ext_map = {"python": ".py", "sql": ".sql", "javascript": ".js", "typescript": ".ts", "shell": ".sh", "txt": ".py"}
    ext = ext_map.get(language, ".py")
    if sol_dir.exists():
        for f in sol_dir.iterdir():
            if f.suffix == ext:
                return f
    fallback = ROOT / "solutions" / slug
    if fallback.exists():
        for f in fallback.iterdir():
            if f.suffix in (".py", ".sql", ".js"):
                return f
    return None


def find_starter(slug, language, questpack_starter):
    if questpack_starter:
        return questpack_starter
    quest_root = ROOT / "data" / "quests" / slug
    ws_dir = quest_root / "workspace"
    ext_map = {"python": ".py", "sql": ".sql", "javascript": ".js"}
    ext = ext_map.get(language, ".py")
    if ws_dir.exists():
        for f in ws_dir.iterdir():
            if f.suffix == ext and not f.name.startswith("example"):
                return f.read_text(encoding="utf-8")
    return None


def load_quests_from_pack(pack_path):
    path = ROOT / pack_path
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("quests", [])
    resolved = []
    for item in data:
        if isinstance(item, dict) and "quest_path" in item and "slug" not in item:
            slug = item["quest_path"].split("/")[-1]
            resolved.append({"slug": slug, "language": "javascript", "starter_code": None})
        else:
            resolved.append(item)
    return resolved


class Results:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.errors = []

    def ok(self, slug, tag):
        self.passed.append(f"{slug} [{tag}]")
        print(f"  OK   {slug} [{tag}]")

    def fail(self, slug, tag, detail):
        self.failed.append(f"{slug} [{tag}]: {detail}")
        print(f"  FAIL {slug} [{tag}]: {detail}")

    def err(self, slug, tag, detail):
        self.errors.append(f"{slug} [{tag}]: {detail}")
        print(f"  WARN {slug} [{tag}]: {detail}")

    def summary(self):
        total = len(self.passed) + len(self.failed) + len(self.errors)
        print("\n" + "=" * 60)
        print(f"SMOKE TEST SUMMARY: {len(self.passed)}/{total} passed")
        if self.failed:
            print(f"\nFAILED ({len(self.failed)}):")
            for f in self.failed:
                print(f"  - {f}")
        if self.errors:
            print(f"\nWARNINGS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  - {e}")
        print("=" * 60)
        return len(self.failed)


def smoke_pack(pack_path, check_starter, results, only_slugs=None):
    print(f"\n--- {pack_path} ---")
    quests = load_quests_from_pack(pack_path)
    for quest in quests:
        slug = quest.get("slug", "")
        if not slug:
            continue
        if only_slugs and slug not in only_slugs:
            continue

        language = quest.get("language", "python")
        if language == "txt":
            language = "python"

        starter_code = quest.get("starter_code")

        sol_path = find_solution(slug, language)
        if sol_path is None:
            results.err(slug, "solution", "no solution file -- skipping")
            continue

        sol_code = sol_path.read_text(encoding="utf-8")

        # Detect if any objective is tests_pass → need mode="tests" to run pytest
        quest_objectives = quest.get("objectives", [])
        has_tests_pass = any(
            (o.get("kind") == "tests_pass" or o.get("id") == "tests_pass")
            for o in quest_objectives
            if isinstance(o, dict)
        )
        run_mode = "tests" if has_tests_pass else "validate"

        resp = post_run(slug, sol_code, language, mode=run_mode)

        if "error" in resp:
            results.err(slug, "solution", str(resp.get("detail", resp["error"]))[:140])
        elif resp.get("passed"):
            results.ok(slug, "solution")
        else:
            obj_failures = [r["id"] for r in resp.get("objective_results", []) if not r.get("ok")]
            results.fail(slug, "solution", f"passed=False, failing={obj_failures}")

        if check_starter:
            starter = find_starter(slug, language, starter_code)
            if starter is None:
                results.err(slug, "starter", "no starter found -- skipping")
                continue
            resp2 = post_run(slug, starter, language, mode=run_mode)
            if "error" in resp2:
                results.err(slug, "starter", str(resp2.get("detail", resp2["error"]))[:140])
            elif not resp2.get("passed"):
                results.ok(slug, "starter-fails")
            else:
                results.fail(slug, "starter", "starter unexpectedly passed all objectives")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8092")
    parser.add_argument("--packs", default="all")
    args = parser.parse_args()

    global BASE_URL
    BASE_URL = args.base_url.rstrip("/")

    results = Results()
    want = set(args.packs.split(","))
    run_all = "all" in want

    if run_all or "python" in want:
        smoke_pack("data/questpacks/foundry_python.json",       check_starter=True,  results=results)
        smoke_pack("data/questpacks/_tier2/python_tier2.json",  check_starter=True,  results=results)
        smoke_pack("data/questpacks/python_systems.json",       check_starter=True,  results=results)

    if run_all or "selenium" in want:
        smoke_pack("data/questpacks/python_selenium.json",      check_starter=False, results=results)

    if run_all or "sql" in want:
        smoke_pack("data/questpacks/sql_core.json",             check_starter=False, results=results)

    if run_all or "js" in want:
        smoke_pack("data/questpacks/javascript_core.json",      check_starter=False, results=results)

    if run_all or "git" in want:
        smoke_pack("data/questpacks/git_core.json",             check_starter=False, results=results)

    if run_all or "ts" in want:
        smoke_pack("data/questpacks/typescript_core.json",      check_starter=False, results=results)

    failures = results.summary()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
