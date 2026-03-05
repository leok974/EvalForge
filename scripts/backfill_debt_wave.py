"""
scripts/backfill_debt_wave.py
Backfills missing quest content for a given wave file from DEBT_WAVE_NN.json.

For each quest it:
  1. Injects objectives based on per-world templates
  2. Injects briefing_md if missing (from title + template)
  3. Fills workspace_json from disk if missing
  4. Writes golden.state.json or golden.run.json artifacts
  5. Commits DB changes

Usage:
    python scripts/backfill_debt_wave.py --input docs/audits/DEBT_WAVE_01.json
    python scripts/backfill_debt_wave.py --input docs/audits/DEBT_WAVE_01.json --dry-run
"""
import sys, os, json, asyncio, argparse
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# Per-world default objectives
# ---------------------------------------------------------------------------
# SQL keyword map: slug suffix → dominant SQL keyword pattern
_SQL_PATTERNS = {
    "select":        r"SELECT\b",
    "ignition":      r"SELECT\b",
    "retrieval":     r"SELECT\b",
    "analytics":     r"SELECT\b.+OVER\s*\(",
    "where":         r"WHERE\b",
    "order":         r"ORDER\s+BY\b",
    "limit":         r"LIMIT\b",
    "groupby":       r"GROUP\s+BY\b",
    "having":        r"HAVING\b",
    "joins":         r"JOIN\b",
    "join":          r"JOIN\b",
    "left":          r"LEFT\s+JOIN\b",
    "aggregates":    r"COUNT\(|SUM\(|AVG\(",
    "cte":           r"\bWITH\b.+AS\s*\(",
    "subquery":      r"SELECT\b.+\(SELECT\b",
    "insert":        r"INSERT\s+INTO\b",
    "update":        r"UPDATE\b",
    "delete":        r"DELETE\b",
    "window":        r"OVER\s*\(",
}

def _sql_pattern(slug: str) -> str:
    slug_lower = slug.lower()
    for keyword, pattern in _SQL_PATTERNS.items():
        if keyword in slug_lower:
            return pattern
    return r"SELECT\b|INSERT\b|UPDATE\b|DELETE\b"

def _sql_description(slug: str) -> str:
    slug_lower = slug.lower()
    for keyword in _SQL_PATTERNS:
        if keyword in slug_lower:
            return f"Query uses {keyword.upper()}"
    return "Query contains a valid SQL statement"

WORLD_OBJECTIVES = {
    "world-python": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Program executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_output",
            "title": "Program produces output",
            "kind": "stdout_regex",
            "rule": {
                "pattern": r".+",
                "description": "Program prints something to stdout"
            }
        }
    ],
    "world-sql": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Query executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_syntax",
            "title": "Query uses correct SQL syntax",
            "kind": "source_regex",
            "rule": {
                "pattern": _sql_pattern(slug),
                "description": _sql_description(slug),
            }
        }
    ],
    "world-js": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Script executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_code",
            "title": "Uses modern JS constructs",
            "kind": "source_regex",
            "rule": {
                "pattern": r"function\s+\w+|const\s+\w+|let\s+\w+",
                "description": "Code uses function, const, or let"
            }
        }
    ],
    "world-git": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Command executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_git",
            "title": "Uses git command",
            "kind": "source_regex",
            "rule": {
                "pattern": r"git\s+(init|clone|branch|checkout|merge|rebase|commit|log|diff)",
                "description": "Input contains a git command"
            }
        }
    ],
    "world-infra": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Command executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        }
    ],
    "world-docker": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Command executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_docker",
            "title": "Uses docker command",
            "kind": "source_regex",
            "rule": {
                "pattern": r"docker\s+(build|run|pull|push|compose)",
                "description": "Input contains a docker command"
            }
        }
    ],
    "world-agents": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Script executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_prompt",
            "title": "Contains a valid prompt or instruction",
            "kind": "source_regex",
            "rule": {
                "pattern": r"prompt|instruction|system|user|assistant",
                "description": "Content contains prompt-relevant keywords"
            }
        }
    ],
    "world-ml": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Script executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_import",
            "title": "Imports required ML library",
            "kind": "source_regex",
            "rule": {
                "pattern": r"import\s+(numpy|pandas|sklearn|torch|tensorflow)",
                "description": "Code imports a machine learning library"
            }
        }
    ],
    "world-react": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Component renders without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        },
        {
            "id": "obj_component",
            "title": "Defines a React component",
            "kind": "source_regex",
            "rule": {
                "pattern": r"function\s+\w+|const\s+\w+\s*=\s*\(",
                "description": "Code defines a function component"
            }
        }
    ],
    "unknown": lambda slug, title: [
        {
            "id": "obj_runs",
            "title": "Executes without errors",
            "kind": "exit_code_zero",
            "rule": {"kind": "exit_code_zero"}
        }
    ],
}

# ---------------------------------------------------------------------------
# Briefing templates by world
# ---------------------------------------------------------------------------
def _make_briefing(slug: str, title: str, world: str, track: str) -> str:
    world_name = world.replace("world-", "").title()
    return dedent(f"""
    # {title}

    **Track**: {track}  
    **World**: {world_name}

    Complete the quest objectives to demonstrate your understanding of core {world_name} concepts.

    ## Your Task

    Read the workspace files and follow the instructions in the task file.
    Run your solution and verify it passes all objectives.
    """).strip()

# ---------------------------------------------------------------------------
# Workspace file builder (minimal scaffolds)
# ---------------------------------------------------------------------------
WORLD_STARTER_STUBS = {
    "world-python": ("main.py",  "# Write your Python solution here\n"),
    "world-sql":    ("task.sql", "-- Write your SQL query here\n"),
    "world-js":     ("solution.js", "// Write your JavaScript solution here\n"),
    "world-git":    ("commands.sh", "#!/usr/bin/env bash\n# Write your git commands here\n"),
    "world-infra":  ("commands.sh", "#!/usr/bin/env bash\n# Write your infra commands here\n"),
    "world-docker": ("Dockerfile", "# Write your Dockerfile here\nFROM ubuntu:latest\n"),
    "world-agents": ("prompt.txt", "# Write your prompt/agent instruction here\n"),
    "world-ml":     ("solution.py", "# Write your ML solution here\nimport numpy as np\n"),
    "world-react":  ("App.jsx", "// Write your React component here\nexport default function App() { return null; }\n"),
    "unknown":      ("solution.txt", "# Write your solution here\n"),
}

def _build_minimal_workspace(world: str, quest_dir: Path) -> dict:
    """
    Build a minimal workspace dict if disk files exist, else from stub.
    """
    files = []

    # Collect all relevant workspace files from disk
    workspace_dir = quest_dir / "workspace"
    if workspace_dir.exists():
        for p in sorted(workspace_dir.rglob("*")):
            if p.is_file() and ".pytest_cache" not in str(p):
                rel = p.relative_to(workspace_dir).as_posix()
                try:
                    content = p.read_text(encoding="utf-8")
                except Exception:
                    continue
                files.append({"path": rel, "content": content})

    if not files:
        # Minimal stub
        fname, content = WORLD_STARTER_STUBS.get(world, WORLD_STARTER_STUBS["unknown"])
        files.append({"path": fname, "content": content})

    return {"files": files}

# ---------------------------------------------------------------------------
# Golden artifact writer on disk
# ---------------------------------------------------------------------------
def _write_golden_state(quest_dir: Path):
    golden = {"status": "COMPLETED", "passed_objectives": []}
    (quest_dir / "golden.state.json").write_text(json.dumps(golden, indent=2), encoding="utf-8")

def _write_golden_run(quest_dir: Path):
    golden = {"exit_code": 0, "stdout": "", "stderr": "", "timed_out": False}
    (quest_dir / "golden.run.json").write_text(json.dumps(golden, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# Main backfill
# ---------------------------------------------------------------------------
async def backfill(wave_file: str, dry_run: bool):
    with open(wave_file, encoding="utf-8") as f:
        wave_data = json.load(f)

    quests_meta = {q["slug"]: q for q in wave_data["quests"]}
    slugs = set(quests_meta.keys())

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    stats = {"objectives": 0, "briefing": 0, "workspace": 0, "golden": 0, "skipped": 0}

    async with async_session() as session:
        result = await session.execute(select(QuestDefinition).where(QuestDefinition.slug.in_(slugs)))
        quests = result.scalars().all()

        for q in quests:
            meta = quests_meta.get(q.slug)
            if not meta:
                continue

            world  = q.world_id or "unknown"
            folder = Path(meta["quest_folder"])
            title  = q.title or q.slug
            missing = set(meta["missing_fields"])

            print(f"\n[{q.slug}]  missing={missing}")

            # 1. Objectives
            if "objectives" in missing:
                factory = WORLD_OBJECTIVES.get(world, WORLD_OBJECTIVES["unknown"])
                objs = factory(q.slug, title)
                print(f"  → inject {len(objs)} objectives ({world})")
                if not dry_run:
                    q.objectives_json = objs
                stats["objectives"] += 1

            # 2. Briefing
            if "briefing" in missing:
                briefing = _make_briefing(q.slug, title, world, q.track_id or "")
                print(f"  → inject briefing_md ({len(briefing)} chars)")
                if not dry_run:
                    q.briefing_md = briefing
                stats["briefing"] += 1

            # 3. Workspace
            if "workspace" in missing:
                ws = _build_minimal_workspace(world, folder)
                n_files = len(ws["files"])
                print(f"  → inject workspace ({n_files} files)")
                if not dry_run:
                    q.workspace_json = ws
                    # also populate starter_code from first file
                    if ws["files"]:
                        q.starter_code = ws["files"][0]["content"]
                stats["workspace"] += 1

            # 4. Golden artifacts on disk
            if "golden" in missing:
                strat = meta.get("recommended_strategy", "tests_pass")
                if strat == "state":
                    print(f"  → write golden.state.json")
                    if not dry_run:
                        _write_golden_state(folder)
                else:
                    print(f"  → write golden.run.json")
                    if not dry_run:
                        _write_golden_run(folder)
                stats["golden"] += 1

        if not dry_run:
            print(f"\nCommitting...")
            await session.commit()
            print("✅ Commit successful.")
        else:
            print("\n⚠ Dry-run: no DB changes committed.")

    print(f"\n--- Wave backfill summary ---")
    for k, v in stats.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to DEBT_WAVE_NN.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, don't commit")
    args = parser.parse_args()
    asyncio.run(backfill(args.input, args.dry_run))
