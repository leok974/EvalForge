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
        "starting_code_path": "data/quests/python/ignition_start.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
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
        "starting_code_path": "data/quests/python/loop_start.py",
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
        "starting_code_path": "data/quests/python/data_forge_start.py",
        "unlocks_boss_id": "reactor-core",
        "unlocks_layout_id": "orion",  # optional: unlock Orion layout here
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Prism (JS) ===
    {
        "slug": "js-light-source",
        "world_id": "world-js",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Light Source",
        "short_description": "Illuminate the basics of JavaScript and the event loop.",
        "detailed_description": (
            "Intro quest for The Prism.\n\n"
            "- Use let/const and functions.\n"
            "- Log diagnostic output.\n"
            "- Wire a basic event handler.\n"
        ),
        "rubric_id": "js_light_source",
        "starting_code_path": "data/quests/js/light_source_start.js",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "js-refraction",
        "world_id": "world-js",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Refraction",
        "short_description": "Bend streams of events into clean, composable logic.",
        "detailed_description": (
            "Boss-prep quest for The Prism.\n\n"
            "- Map and filter arrays of events.\n"
            "- Normalize payloads.\n"
            "- Build the reducer that feeds The Signal Prism boss.\n"
        ),
        "rubric_id": "js_refraction",
        "starting_code_path": "data/quests/js/refraction_start.js",
        "unlocks_boss_id": "signal-prism",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Archives (SQL) ===
    {
        "slug": "sql-retrieval",
        "world_id": "world-sql",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Retrieval",
        "short_description": "Learn to fetch data from the Archives with SELECT.",
        "detailed_description": (
            "Intro quest for The Archives.\n\n"
            "- Basic SELECT queries.\n"
            "- Simple WHERE filters.\n"
            "- LIMIT and ORDER BY.\n"
        ),
        "rubric_id": "sql_retrieval",
        "starting_code_path": "data/quests/sql/retrieval.sql",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "sql-filter",
        "world_id": "world-sql",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Filter",
        "short_description": "Control the Archive’s flow with precise filters and joins.",
        "detailed_description": (
            "Boss-prep quest for The Archives.\n\n"
            "- Combine WHERE, AND/OR.\n"
            "- Use INNER JOIN.\n"
            "- Build the query The Archive Warden boss will test.\n"
        ),
        "rubric_id": "sql_filter",
        "starting_code_path": "data/quests/sql/filter.sql",
        "unlocks_boss_id": "archive-warden",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Grid (Infra) ===
    {
        "slug": "infra-containment",
        "world_id": "world-infra",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Containment",
        "short_description": "Learn how to containerize a simple service safely.",
        "detailed_description": (
            "Intro quest for The Grid.\n\n"
            "- Write a basic Dockerfile.\n"
            "- Expose a health endpoint.\n"
            "- Run locally and verify.\n"
        ),
        "rubric_id": "infra_containment",
        "starting_code_path": "data/quests/infra/containment.Dockerfile",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "infra-service-link",
        "world_id": "world-infra",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Service Link",
        "short_description": "Wire services together so The Grid Sentinel can test resilience.",
        "detailed_description": (
            "Boss-prep quest for The Grid.\n\n"
            "- Compose multiple services.\n"
            "- Configure health checks.\n"
            "- Verify a simple request path through the grid.\n"
        ),
        "rubric_id": "infra_service_link",
        "starting_code_path": "data/quests/infra/service_link.docker-compose.yml",
        "unlocks_boss_id": "grid-sentinel",
        "unlocks_layout_id": "workshop",  # optional: unlock Workshop here
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Oracle (Agents) ===
    {
        "slug": "agents-invocation",
        "world_id": "world-agents",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Invocation",
        "short_description": "Call a single agent with a safe, well-typed prompt.",
        "detailed_description": (
            "Intro quest for The Oracle.\n\n"
            "- Call the LLM with a JSON schema.\n"
            "- Handle errors gracefully.\n"
            "- Log traces for debugging.\n"
        ),
        "rubric_id": "agents_invocation",
        "starting_code_path": "data/quests/agents/invocation_start.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "agents-grounding",
        "world_id": "world-agents",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Grounding",
        "short_description": "Ground your agent with tools and RAG before it faces the Oracle Mirror.",
        "detailed_description": (
            "Boss-prep quest for The Oracle.\n\n"
            "- Add a tool (HTTP/DB).\n"
            "- Use RAG for citations.\n"
            "- Enforce guardrails before the boss.\n"
        ),
        "rubric_id": "agents_grounding",
        "starting_code_path": "data/quests/agents/grounding_start.py",
        "unlocks_boss_id": "oracle-mirror",
        "unlocks_layout_id": None,
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },

    # === The Timeline (Git) ===
    {
        "slug": "git-commit",
        "world_id": "world-git",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Commit",
        "short_description": "Capture a clean snapshot in the Timeline with proper commits.",
        "detailed_description": (
            "Intro quest for The Timeline.\n\n"
            "- Initialize a repo.\n"
            "- Stage and commit changes.\n"
            "- Write a meaningful commit message.\n"
        ),
        "rubric_id": "git_commit",
        "starting_code_path": "data/quests/git/commit_start.txt",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "git-branch",
        "world_id": "world-git",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Branch",
        "short_description": "Branch, merge, and resolve conflicts before facing the Timeline Hydra.",
        "detailed_description": (
            "Boss-prep quest for The Timeline.\n\n"
            "- Create and switch branches.\n"
            "- Merge changes.\n"
            "- Resolve a simple conflict.\n"
        ),
        "rubric_id": "git_branch",
        "starting_code_path": "data/quests/git/branch_start.txt",
        "unlocks_boss_id": "timeline-hydra",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
    },

    # === The Synapse (ML) ===
    {
        "slug": "ml-tensor",
        "world_id": "world-ml",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Tensor",
        "short_description": "Get comfortable with tensors, shapes, and basic operations.",
        "detailed_description": (
            "Intro quest for The Synapse.\n\n"
            "- Create tensors.\n"
            "- Inspect shapes.\n"
            "- Perform basic arithmetic ops.\n"
        ),
        "rubric_id": "ml_tensor",
        "starting_code_path": "data/quests/ml/tensor_start.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 50,
        "mastery_xp_bonus": 20,
    },
    {
        "slug": "ml-gradient",
        "world_id": "world-ml",
        "track_id": "boss-prep",
        "order_index": 20,
        "title": "Gradient",
        "short_description": "Train a tiny model and watch gradients flow before Synapse Colossus.",
        "detailed_description": (
            "Boss-prep quest for The Synapse.\n\n"
            "- Define a simple model.\n"
            "- Run a forward/backward pass.\n"
            "- Inspect loss improvements.\n"
        ),
        "rubric_id": "ml_gradient",
        "starting_code_path": "data/quests/ml/gradient_start.py",
        "unlocks_boss_id": "synapse-colossus",
        "unlocks_layout_id": None,
        "base_xp_reward": 70,
        "mastery_xp_bonus": 30,
    },
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
