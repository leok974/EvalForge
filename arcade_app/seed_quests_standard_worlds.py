# arcade_app/seed_quests_standard_worlds.py
from __future__ import annotations
import json
import os
from pathlib import Path

from typing import List, Dict, Any

from sqlalchemy.orm import Session

from arcade_app.models import QuestDefinition


STANDARD_QUESTLINES: List[Dict[str, Any]] = [
    # === The Foundry (Python) ===
    {
        "slug": "first-sparks",
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
        "slug": "hello-variable",
        "world_id": "world-python",
        "track_id": "fundamentals",
        "order_index": 15,
        "title": "Hello Variable",
        "short_description": "Learn variable assignment basics.",
        "detailed_description": "First Python quest: define a variable and assign a value.",
        "rubric_id": "python_hello",
        "starting_code_path": "data/quests/hello-variable/workspace/main.py",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 30,
        "mastery_xp_bonus": 10,
        "objectives_json": [
            {
                "id": "obj_var_energy",
                "kind": "ast",
                "rule": {
                    "kind": "ast",
                    "must_assign_variable": "energy"
                },
                "text": "Define variable 'energy'",
                "why": "Practice variable assignment"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {
                    "kind": "exit_code_zero"
                },
                "text": "Code runs without errors",
                "why": "Ensure syntax is correct"
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
        "objectives_json": [
            {
                "id": "obj_define_function",
                "kind": "ast",
                "rule": {
                    "kind": "ast",
                    "must_define_function": "generate_evens"
                },
                "text": "Define function generate_evens",
                "why": "Learn function definition syntax"
            },
            {
                "id": "obj_stdout",
                "kind": "stdout_exact",
                "rule": {
                    "kind": "stdout_exact",
                    "expected": "2,4,6,8,10"  # From golden.json - CANONICAL: use 'expected' not 'pattern'
                },
                "text": "Output correct comma-separated evens",
                "why": "Verify loop logic produces expected output"
            },
            {
                "id": "obj_tests",
                "kind": "tests_pass",
                "rule": {
                    "kind": "tests_pass"
                },
                "text": "Pass all unit tests",
                "why": "Verify generate_evens works for edge cases"
            }
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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
        "objectives_json": [
            {
                "id": "obj_load_sales",
                "kind": "ast",
                "rule": {
                    "kind": "ast",
                    "must_define_function": "load_sales"
                },
                "text": "Define function load_sales",
                "why": "Learn CSV file reading and parsing"
            },
            {
                "id": "obj_revenue_by_item",
                "kind": "ast",
                "rule": {
                    "kind": "ast",
                    "must_define_function": "revenue_by_item"
                },
                "text": "Define function revenue_by_item",
                "why": "Learn dictionary aggregation patterns"
            },
            {
                "id": "obj_top_items",
                "kind": "ast",
                "rule": {
                    "kind": "ast",
                    "must_define_function": "top_items"
                },
                "text": "Define function top_items",
                "why": "Learn sorting with custom keys"
            },
            {
                "id": "obj_stdout",
                "kind": "stdout_regex",
                "rule": {
                    "kind": "stdout_regex",
                    "pattern": "apple=10\\.50\\s*\\nbanana=6\\.40",
                    "description": "Top 2 items with revenue (apple=10.50, banana=6.40)"
                },
                "text": "Output top 2 items correctly formatted",
                "why": "Verify complete data pipeline works"
            }
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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
        "objectives_json": [
            {
                "id": "obj_define_function",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "function\\s+\\w+"
                },
                "text": "Define a JavaScript function",
                "why": "Learn function syntax in JS"
            },
            {
                "id": "obj_console_log",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "console\\.log"
                },
                "text": "Use console.log",
                "why": "Learn console output in JS"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Code runs without errors",
                "why": "Ensure syntax is correct"
            }
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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
        "objectives_json": [
            {
                "id": "obj_use_const",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "const\\s+\\w+"
                },
                "text": "Use const declaration",
                "why": "Learn modern variable declarations"
            },
            {
                "id": "obj_use_let",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "let\\s+\\w+"
                },
                "text": "Use let declaration",
                "why": "Learn block-scoped variables"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Code runs without errors",
                "why": "Ensure syntax is correct"
            }
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
    },

    # === The Archives (SQL) ===

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
        "objectives_json": [
            {
                "id": "obj_docker_cmd",
                "kind": "source_regex",
                "rule": {"kind": "source_regex", "pattern": "docker|FROM"},
                "text": "Use Docker commands",
                "why": "Learn container basics"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Configuration valid",
                "why": "Ensure syntax correct"
            }
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {
                "id": "obj_port",
                "kind": "source_regex",
                "rule": {"kind": "source_regex", "pattern": "port|localhost"},
                "text": "Configure ports/localhost",
                "why": "Learn networking"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Config runs successfully",
                "why": "Ensure valid setup"
            }
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {"id": "obj_agent", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "agent|llm|model"}, "text": "Use agent/LLM", "why": "Learn agent basics"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Runs successfully", "why": "Ensure syntax correct"}
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {"id": "obj_contract", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "contract|schema|type"}, "text": "Define contract", "why": "Learn structured prompts"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Runs successfully", "why": "Ensure valid"}
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {"id": "obj_git_init", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "git\\s+(init|clone)"}, "text": "Use git init or clone", "why": "Learn repo initialization"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Command succeeds", "why": "Ensure syntax correct"}, {'id': 'fs_snapshot', 'title': 'Verify file structure', 'kind': 'fs_snapshot', 'rule': {'must_exist': ['README.md', 'main.py', 'task.sh']}}, {'id': 'git_status_clean', 'title': 'Verify git status', 'kind': 'git_status_clean', 'rule': {'expected_porcelain': '?? main.py\n?? task.sh'}}, {'id': 'git_log_contains', 'title': 'Verify commit history', 'kind': 'git_log_contains', 'rule': {'must_contain': ['a731329 Initial commit'], 'min_commits': 1}}
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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
        "objectives_json": [
            {"id": "obj_git_clone", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "git\\s+clone"}, "text": "Use git clone", "why": "Learn repository cloning"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Command succeeds", "why": "Ensure valid"}, {'id': 'fs_snapshot', 'title': 'Verify file structure', 'kind': 'fs_snapshot', 'rule': {'must_exist': ['README.md', 'fixtures/hello.txt', 'main.py', 'outputs/report.json', 'sandbox/clone/hello.txt', 'sandbox/remote.git/HEAD', 'sandbox/remote.git/config', 'sandbox/remote.git/description', 'sandbox/remote.git/hooks/applypatch-msg.sample', 'sandbox/remote.git/hooks/commit-msg.sample', 'sandbox/remote.git/hooks/fsmonitor-watchman.sample', 'sandbox/remote.git/hooks/post-update.sample', 'sandbox/remote.git/hooks/pre-applypatch.sample', 'sandbox/remote.git/hooks/pre-commit.sample', 'sandbox/remote.git/hooks/pre-merge-commit.sample', 'sandbox/remote.git/hooks/pre-push.sample', 'sandbox/remote.git/hooks/pre-rebase.sample', 'sandbox/remote.git/hooks/pre-receive.sample', 'sandbox/remote.git/hooks/prepare-commit-msg.sample', 'sandbox/remote.git/hooks/push-to-checkout.sample', 'sandbox/remote.git/hooks/sendemail-validate.sample', 'sandbox/remote.git/hooks/update.sample', 'sandbox/remote.git/info/exclude', 'sandbox/remote.git/objects/61/d679ca3bdc447b77658937e49e0f617dd07927', 'sandbox/remote.git/objects/ef/0493b275aa2080237f676d2ef6559246f56636', 'sandbox/remote.git/objects/f6/dec98feb4f9658abd72f82961dbf5978d0034b', 'sandbox/remote.git/refs/heads/main', 'sandbox/repo/hello.txt', 'task.sh', 'task.txt', 'test_public.py', 'wrapper.sh']}}
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {"id": "obj_ml_lib", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "import\\s+(numpy|pandas|sklearn|tensorflow|torch)"}, "text": "Import ML library", "why": "Learn ML environment setup"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Runs successfully", "why": "Ensure valid"}
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
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
        "objectives_json": [
            {"id": "obj_numpy", "kind": "source_regex", "rule": {"kind": "source_regex", "pattern": "np\\.|numpy"}, "text": "Use NumPy", "why": "Learn arrays"},
            {"id": "obj_exit_zero", "kind": "exit_code_zero", "rule": {"kind": "exit_code_zero"}, "text": "Runs successfully", "why": "Ensure valid"}
        ],
        "runtime_rules_json": {"enabled": True, "require_exit_code_zero": True, "require_no_timeout": True}
    },
]



def load_questpacks() -> List[Dict[str, Any]]:
    """Loads all questpacks defined in data/questpacks/*.json"""
    packs = [
        "data/questpacks/sql_core.json",
        "data/questpacks/_tier2/sql_tier2.json",
        "data/questpacks/sql_tier3/sql_tier3.json"
    ]
    all_quests = []
    for p in packs:
        if not os.path.exists(p):
            print(f"WARNING: Questpack not found: {p}")
            continue
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Questpacks might have global world_id/track_id
            global_world = data.get("world_id")
            global_track = data.get("track_id")
            for q in data.get("quests", []):
                if global_world and "world_id" not in q:
                    q["world_id"] = global_world
                if global_track and "track_id" not in q:
                    q["track_id"] = global_track
                
                # Format transition: 'objectives' -> 'objectives_json'
                if "objectives" in q:
                    q["objectives_json"] = q.pop("objectives")
                # Format transition: 'description' -> 'short_description'
                if "description" in q and "short_description" not in q:
                    q["short_description"] = q.pop("description")
                
                all_quests.append(q)
    return all_quests

def validate_strict(cfg: Dict[str, Any]) -> List[str]:
    """Strict validation for required quest fields to prevent silent drift."""
    errors = []
    required = ["slug", "world_id", "track_id", "order_index", "title", "short_description"]
    for field in required:
        if not cfg.get(field):
            errors.append(f"Missing required field: '{field}'")
    
    # SQL specific strictness
    if cfg.get("world_id") == "world-sql":
        if cfg.get("language") != "sql":
            errors.append(f"SQL quest must have 'language: sql'")
        
        # Check workspace entrypoint if starting_code_path is provided
        start_path = cfg.get("starting_code_path")
        if start_path and not os.path.exists(start_path):
             errors.append(f"Starting code path does not exist: {start_path}")
             
        # Check objectives (must have at least one)
        objs = cfg.get("objectives_json", [])
        if not objs:
            errors.append(f"Quest must have at least one objective")
            
    return errors

def seed_standard_world_quests(db: Session, validate_only: bool = False) -> None:
    """
    Idempotently seed/update questlines for the 7 core worlds.
    If validate_only is True, checks schema without writing to DB.
    """
    validation_errors = []
    
    # Combine static list + dynamic questpacks
    all_configs = STANDARD_QUESTLINES + load_questpacks()
    
    # Strict mode toggle (could be env var)
    STRICT_MODE = os.getenv("EF_SEED_STRICT", "true").lower() == "true"
    
    for cfg in all_configs:
        slug = cfg["slug"]
        
        # 1. Strict Metadata Check
        strict_errors = validate_strict(cfg)
        if strict_errors:
            msg = f"STRICT ERROR in quest '{slug}': {'; '.join(strict_errors)}"
            if STRICT_MODE:
                if validate_only:
                    validation_errors.append(msg)
                else:
                    raise ValueError(msg)
            else:
                 print(f"WARNING: {msg}")

        # 2. Validate Objectives Schema (Seed-Time Gate)
        objectives = cfg.get("objectives_json", [])
        if objectives:
            from arcade_app.services.quest_validate import audit_objective_schema
            for obj in objectives:
                errors = audit_objective_schema(obj)
                if errors:
                    msg = f"CRITICAL: Invalid Objective in quest '{slug}' (Objective ID: {obj.get('id')}): {', '.join(errors)}"
                    if validate_only:
                        validation_errors.append(msg)
                    else:
                        raise ValueError(msg)
        
        # 3. Disk-based Doc Rehydration (Phase 9.8 Strategy)
        start_path = cfg.get("starting_code_path")
        if start_path:
            # starting_code_path: data/quests/sql-order-by/workspace/task.sql
            # quest_base_dir: data/quests/sql-order-by
            quest_base_dir = Path(start_path).parent.parent
            docs_dir = quest_base_dir / "docs"
            if docs_dir.exists():
                tutorial_file = docs_dir / "tutorial.md"
                if tutorial_file.exists():
                    cfg["tutorial_md"] = tutorial_file.read_text(encoding="utf-8")
                
                briefing_file = docs_dir / "briefing.md"
                if briefing_file.exists():
                    cfg["briefing_md"] = briefing_file.read_text(encoding="utf-8")
                
                lore_file = docs_dir / "lore.md"
                if lore_file.exists():
                    cfg["lore_md"] = lore_file.read_text(encoding="utf-8")
                
                debrief_file = docs_dir / "debrief.md"
                if debrief_file.exists():
                    cfg["debrief_md"] = debrief_file.read_text(encoding="utf-8")
                
                hints_file = docs_dir / "hints.md"
                if hints_file.exists():
                    # Check if hints are already in tiered_hints_json
                    if not cfg.get("tiered_hints_json"):
                        # If hints.md exists, we might want to store it or parse it
                        # For now, let's treat it as a raw doc if not already structured
                        cfg["hints_md"] = hints_file.read_text(encoding="utf-8")

            # 4. Workspace Rehydration
            quest_workspace_dir = Path(start_path).parent
            if quest_workspace_dir.exists() and not cfg.get("workspace_json"):
                workspace_files = []
                for file_path in quest_workspace_dir.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(quest_workspace_dir).as_posix()
                        # Skip common ignore patterns
                        if ".pytest_cache" in rel_path or "golden.run.json" in rel_path:
                            continue
                        try:
                            content = file_path.read_text(encoding="utf-8")
                            workspace_files.append({
                                "path": rel_path,
                                "content": content,
                                "editable": not rel_path.startswith("fixtures/")
                            })
                        except Exception:
                            continue
                if workspace_files:
                    cfg["workspace_json"] = {"files": workspace_files}

        if validate_only:
             continue

        existing = (
            db.query(QuestDefinition)
            .filter(QuestDefinition.slug == slug)
            .one_or_none()
        )
        if existing:
            # Update fields if they changed (safe for dev iteration)
            existing.world_id = cfg.get("world_id")
            existing.track_id = cfg.get("track_id")
            existing.order_index = cfg.get("order_index")
            existing.title = cfg.get("title")
            existing.short_description = cfg.get("short_description")
            existing.detailed_description = cfg.get("detailed_description", "")
            existing.rubric_id = cfg.get("rubric_id")
            existing.starting_code_path = cfg.get("starting_code_path")
            existing.unlocks_boss_id = cfg.get("unlocks_boss_id")
            existing.unlocks_layout_id = cfg.get("unlocks_layout_id")
            existing.base_xp_reward = cfg.get("base_xp_reward", 50)
            existing.mastery_xp_bonus = cfg.get("mastery_xp_bonus", 0)
            existing.objectives_json = objectives # Explicitly update objectives
            existing.language = cfg.get("language", "python")
            if "workspace_json" in cfg:
                existing.workspace_json = cfg["workspace_json"]
            if "key_terms" in cfg:
                existing.key_terms = cfg["key_terms"]
            if "concept_tags" in cfg:
                existing.concept_tags = cfg["concept_tags"]
            if "codex_references" in cfg:
                existing.codex_references = cfg["codex_references"]
            if "workspace_json" in cfg:
                existing.workspace_json = cfg["workspace_json"]
            
            # Phase 9: Database Workbench Fields
            if "db_engine" in cfg:
                existing.db_engine = cfg["db_engine"]
            if "db_explorer_enabled" in cfg:
                existing.db_explorer_enabled = cfg["db_explorer_enabled"]
            if "db_allow_mutation" in cfg:
                existing.db_allow_mutation = cfg["db_allow_mutation"]
            
            # Rehydrated docs
            if "tutorial_md" in cfg:
                existing.tutorial_md = cfg["tutorial_md"]
            if "briefing_md" in cfg:
                existing.briefing_md = cfg["briefing_md"]
            if "lore_md" in cfg:
                existing.lore_md = cfg["lore_md"]
            if "debrief_md" in cfg:
                existing.debrief_md = cfg["debrief_md"]
            
            # Phase 11: Explorer Scoping
            if "db_explorer_mode" in cfg:
                existing.db_explorer_mode = cfg["db_explorer_mode"]
            if "featured_tables" in cfg:
                existing.featured_tables = cfg["featured_tables"]
            if "related_tables" in cfg:
                existing.related_tables = cfg["related_tables"]
            if "hidden_tables" in cfg:
                existing.hidden_tables = cfg["hidden_tables"]

            if "hints_md" in cfg:
                existing.tiered_hints_json = {"markdown_source": cfg["hints_md"]}
        else:
            q = QuestDefinition(
                slug=slug,
                world_id=cfg.get("world_id"),
                track_id=cfg.get("track_id"),
                order_index=cfg.get("order_index"),
                title=cfg.get("title"),
                short_description=cfg.get("short_description"),
                detailed_description=cfg.get("detailed_description", ""),
                rubric_id=cfg.get("rubric_id"),
                starting_code_path=cfg.get("starting_code_path"),
                unlocks_boss_id=cfg.get("unlocks_boss_id"),
                unlocks_layout_id=cfg.get("unlocks_layout_id"),
                base_xp_reward=cfg.get("base_xp_reward", 50),
                mastery_xp_bonus=cfg.get("mastery_xp_bonus", 0),
                objectives_json=objectives,
                language=cfg.get("language", "python"),
                workspace_json=cfg.get("workspace_json", {}),
                key_terms=cfg.get("key_terms", []),
                concept_tags=cfg.get("concept_tags", []),
                codex_references=cfg.get("codex_references", []),
                tutorial_md=cfg.get("tutorial_md"),
                briefing_md=cfg.get("briefing_md"),
                lore_md=cfg.get("lore_md"),
                debrief_md=cfg.get("debrief_md"),
                tiered_hints_json={"markdown_source": cfg["hints_md"]} if "hints_md" in cfg else cfg.get("tiered_hints_json", {}),
                # Phase 9: Database Workbench Fields
                db_engine=cfg.get("db_engine", "sqlite"),
                db_explorer_enabled=cfg.get("db_explorer_enabled", False),
                db_allow_mutation=cfg.get("db_allow_mutation", False),
                # Phase 11: Explorer Scoping
                db_explorer_mode=cfg.get("db_explorer_mode", "full"),
                featured_tables=cfg.get("featured_tables", []),
                related_tables=cfg.get("related_tables", []),
                hidden_tables=cfg.get("hidden_tables", []),
            )
            db.add(q)

    if validate_only:
        if validation_errors:
            for err in validation_errors:
                print(err)
            raise ValueError(f"Validation Failed: {len(validation_errors)} errors found.")
        else:
            print(f"✅ Validation Passed: Checked {len(STANDARD_QUESTLINES)} quests.")
            return

    db.commit()


if __name__ == "__main__":
    import asyncio
    from arcade_app.database import engine
    from arcade_app.config import DATABASE_URL
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine as create_sync_engine
    
    # We need a sync engine for the seeder which uses a sync Session
    if "postgresql" in DATABASE_URL:
        SYNC_URL = DATABASE_URL.replace("asyncpg", "psycopg2")
    elif "sqlite" in DATABASE_URL:
        SYNC_URL = DATABASE_URL.replace("+aiosqlite", "")
    else:
        SYNC_URL = DATABASE_URL
        
    sync_engine = create_sync_engine(SYNC_URL)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
    db = SessionLocal()
    try:
        seed_standard_world_quests(db)
        print("✅ Seeding complete.")
    finally:
        db.close()
