# arcade_app/seed_quests_standard_worlds.py
from __future__ import annotations

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
    {
        "slug": "sql-ignition",
        "world_id": "world-sql",
        "track_id": "fundamentals",
        "order_index": 10,
        "title": "Ignition",
        "short_description": "Start your SQL engine.",
        "detailed_description": "Basic SQL selection.",
        "rubric_id": "sql_ignition",
        "starting_code_path": "data/quests/sql-ignition/workspace/task.sql",
        "unlocks_boss_id": None,
        "unlocks_layout_id": None,
        "base_xp_reward": 40,
        "mastery_xp_bonus": 20,
        "objectives_json": [
            {
                "id": "obj_select_statement",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "SELECT.*FROM"
                },
                "text": "Write SELECT FROM query",
                "why": "Learn basic SQL query structure"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Query executes successfully",
                "why": "Ensure SQL syntax is correct"
            }, {'id': 'fs_snapshot', 'title': 'Verify file structure', 'kind': 'fs_snapshot', 'rule': {'must_exist': ['README.md', 'fixtures/schema.sql', 'fixtures/seed.sql', 'main.py', 'task.sql']}}
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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
        "starting_code_path": "data/quests/sql-select/workspace/task.sql",
        "unlocks_boss_id": "archive-warden",
        "unlocks_layout_id": None,
        "base_xp_reward": 60,
        "mastery_xp_bonus": 25,
        "objectives_json": [
            {
                "id": "obj_join",
                "kind": "source_regex",
                "rule": {
                    "kind": "source_regex",
                    "pattern": "JOIN"
                },
                "text": "Use JOIN clause",
                "why": "Learn table joins"
            },
            {
                "id": "obj_exit_zero",
                "kind": "exit_code_zero",
                "rule": {"kind": "exit_code_zero"},
                "text": "Query executes successfully",
                "why": "Ensure syntax is correct"
            }, {'id': 'fs_snapshot', 'title': 'Verify file structure', 'kind': 'fs_snapshot', 'rule': {'must_exist': ['README.md', 'fixtures/schema.sql', 'fixtures/seed.sql', 'main.py', 'task.sql']}}
        ],
        "runtime_rules_json": {
            "enabled": True,
            "require_exit_code_zero": True,
            "require_no_timeout": True
        }
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



def seed_standard_world_quests(db: Session, validate_only: bool = False) -> None:
    """
    Idempotently seed/update questlines for the 7 core worlds.
    If validate_only is True, checks schema without writing to DB.
    """
    validation_errors = []
    
    for cfg in STANDARD_QUESTLINES:
        slug = cfg["slug"]
        
        # Validate Objectives Schema (Seed-Time Gate)
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
        
        if validate_only:
             continue

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
            existing.objectives_json = objectives # Explicitly update objectives
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
                objectives_json=objectives
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
