# arcade_app/seed_quests_standard_worlds.py
from __future__ import annotations

from typing import List, Dict, Any

from sqlalchemy.orm import Session

from arcade_app.models import QuestDefinition


STANDARD_QUESTLINES: List[Dict[str, Any]] = [
    # === The Foundry (Python) ===
    {
        "slug": "python-ignition",
        "world_id": "world-python",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Boot up your Python engine with prints, variables, and expressions.",
        "detailed_description": (
            "Warm-up quest for The Foundry.\n\n"
            "- Write your first Python script.\n"
            "- Use variables, strings, and basic arithmetic.\n"
            "- Print a status line that matches the spec.\n"
        ),
        "rubric_id": "python_ignition",
        "starting_code_path": "data/quests/python-ignition/workspace/task.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
        "objectives_json": [
            {
                "id": "obj_runs",
                "title": "Program executes successfully",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"}
            },
            {
                "id": "obj_output",
                "title": "Print correct message",
                "kind": "stdout_regex",
                "rule": {
                    "kind": "stdout_regex",
                    "pattern": "System Online",
                    "description": "Output containing 'System Online'"
                }
            }
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
    },
    {
        "slug": "python-loop",
        "world_id": "world-python",
        "track_id": "fundamentals",
        "order_index": 20,
        "title": "Loop",
        "short_description": "Learn loops and conditionals to process collections of data.",
        "detailed_description": (
            "Second quest in The Foundry arc.\n\n"
            "- Use for/while loops.\n"
            "- Filter values with if/else.\n"
            "- Build a simple report over a list of records.\n"
        ),
        "rubric_id": "python_loop",
        "starting_code_path": "data/quests/python-loop/workspace/task.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "python-data-forge",
        "world_id": "world-python",
        "track_id": "boss-prep",
        "order_index": 30,
        "title": "Data Forge",
        "short_description": "Shape messy data into something Reactor Core can consume.",
        "detailed_description": (
            "Boss-prep quest for The Foundry.\n\n"
            "- Parse input records (JSON/CSV).\n"
            "- Normalize into a consistent schema.\n"
            "- Emit a summary object used by The Reactor Core boss.\n"
        ),
        "rubric_id": "python_data_forge",
        "starting_code_path": "data/quests/python-data-forge/workspace/task.py",
        "unlocks_boss_id": "reactor-core",
        "unlocks_layout_id": "orion",  # optional: unlock Orion layout here
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Prism (JS) ===
    {
        "slug": "js-ignition-q1-console-and-functions",
        "world_id": "world-js",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition: Console & Functions",
        "short_description": "First sparks of JavaScript.",
        "detailed_description": "Initial JS quest.",
        "rubric_id": "js_ignition",
        "starting_code_path": "data/quests/js-ignition-q1-console-and-functions/workspace/main.js",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "js-vars-q1-let-const-var",
        "world_id": "world-js",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Variables: Let, Const, Var",
        "short_description": "Master variable declarations.",
        "detailed_description": "Variable scoping quest.",
        "rubric_id": "js_vars",
        "starting_code_path": "data/quests/js-vars-q1-let-const-var/workspace/main.js",
        "unlocks_boss_id": "signal-prism",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Archives (SQL) ===
    {
        "slug": "sql-ignition",
        "world_id": "world-sql",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Start your SQL engine.",
        "detailed_description": "Basic SQL selection.",
        "rubric_id": "sql_ignition",
        "starting_code_path": "data/quests/sql-ignition/workspace/query.sql",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "sql-select",
        "world_id": "world-sql",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Selection",
        "short_description": "Refine your data retrieval.",
        "detailed_description": "Advanced SELECT.",
        "rubric_id": "sql_select",
        "starting_code_path": "data/quests/sql-select/workspace/query.sql",
        "unlocks_boss_id": "archive-warden",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Grid (Infra) ===
    {
        "slug": "infra-ignition",
        "world_id": "world-infra",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Preflight checks for The Grid.",
        "detailed_description": "Infrastructure ignition.",
        "rubric_id": "infra_ignition",
        "starting_code_path": "data/quests/infra-ignition/workspace/task.sh",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "infra-ports-and-localhost",
        "world_id": "world-infra",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Ports & Localhost",
        "short_description": "Understand connectivity.",
        "detailed_description": "Port mapping quest.",
        "rubric_id": "infra_ports",
        "starting_code_path": "data/quests/infra-ports-and-localhost/workspace/task.sh",
        "unlocks_boss_id": "grid-sentinel",
        "unlocks_layout_id": "workshop",
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Oracle (Agents) ===
    {
        "slug": "agents-ignition",
        "world_id": "world-agents",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Awaken the Oracle.",
        "detailed_description": "Agent first steps.",
        "rubric_id": "agents_ignition",
        "starting_code_path": "data/quests/agents-ignition/workspace/main.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "agents-prompts-contracts",
        "world_id": "world-agents",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Prompts & Contracts",
        "short_description": "Define the interface.",
        "detailed_description": "Prompt engineering basics.",
        "rubric_id": "agents_prompts",
        "starting_code_path": "data/quests/agents-prompts-contracts/workspace/main.py",
        "unlocks_boss_id": "oracle-mirror",
        "unlocks_layout_id": None,
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Timeline (Git) ===
    {
        "slug": "git-ignition",
        "world_id": "world-git",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Initialize your Timeline.",
        "detailed_description": "Git init basics.",
        "rubric_id": "git_ignition",
        "starting_code_path": "data/quests/git-ignition/workspace/task.sh",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "git-init-clone",
        "world_id": "world-git",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Init & Clone",
        "short_description": "Cloning the history.",
        "detailed_description": "Git clone operations.",
        "rubric_id": "git_init_clone",
        "starting_code_path": "data/quests/git-init-clone/workspace/task.sh",
        "unlocks_boss_id": "timeline-hydra",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Synapse (ML) ===
    {
        "slug": "ml-ignition",
        "world_id": "world-ml",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Spark the synapse.",
        "detailed_description": "ML basics.",
        "rubric_id": "ml_ignition",
        "starting_code_path": "data/quests/ml-ignition/workspace/task.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "ml-numpy-basics",
        "world_id": "world-ml",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Numpy Basics",
        "short_description": "Matrix operations.",
        "detailed_description": "Numpy foundations.",
        "rubric_id": "ml_numpy",
        "starting_code_path": "data/quests/ml-numpy-basics/workspace/task.py",
        "unlocks_boss_id": "synapse-colossus",
        "unlocks_layout_id": None,
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    }
]


def seed_standard_world_quests(db: Session) -> None:
    """
    Idempotently seed/update questlines for the 7 core worlds.
    """
    for cfg in STANDARD_QUESTLINES:
        slug = cfg["slug"]
        existing = (
            db.query(QuestDefinition)
            .filter(QuestDefinition.slug == slug)
            .one_or_none()
        )
        if existing:
            # Update fields if they changed (safe for dev iteration)
            existing.world_id = cfg["world_id"]
            existing.track_id = cfg["track_id"]
            existing.order_index = cfg["order_index"]
            existing.title = cfg["title"]
            existing.short_description = cfg["short_description"]
            existing.detailed_description = cfg["detailed_description"]
            existing.rubric_id = cfg["rubric_id"]
            existing.starting_code_path = cfg["starting_code_path"]
            existing.unlocks_boss_id = cfg["unlocks_boss_id"]
            existing.unlocks_layout_id = cfg["unlocks_layout_id"]
            existing.base_xp_reward = cfg["base_xp_reward"]
            existing.mastery_xp_bonus = cfg["mastery_xp_bonus"]
        else:
            q = QuestDefinition(
                slug=slug,
                world_id=cfg["world_id"],
                track_id=cfg["track_id"],
                order_index=cfg["order_index"],
                title=cfg["title"],
                short_description=cfg["short_description"],
                detailed_description=cfg["detailed_description"],
                rubric_id=cfg["rubric_id"],
                starting_code_path=cfg["starting_code_path"],
                unlocks_boss_id=cfg["unlocks_boss_id"],
                unlocks_layout_id=cfg["unlocks_layout_id"],
                base_xp_reward=cfg["base_xp_reward"],
                mastery_xp_bonus=cfg["mastery_xp_bonus"],
            )
            db.add(q)

    db.commit()
