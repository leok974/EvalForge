# arcade_app/questmaster.py
"""
QuestMaster agent: generates project-specific questlines from codex analysis.
"""
import os
from sqlalchemy.orm import Session
from arcade_app.models import Project
from arcade_app.project_questline_spec import ProjectQuestlineSpec


# Golden spec for ApplyLens (hand-crafted reference implementation)
APPLYLENS_QUESTLINE_GOLDEN = {
    "project_slug": "applylens",
    "project_name": "ApplyLens",
    "template": "fullstack_saas_agents",
    "tracks": [
        {
            "track_id": "project-fundamentals",
            "label": "Core System",
            "order_index": 10,
            "quests": [
                {
                    "slug": "applylens-core-tour",
                    "title": "System Tour: ApplyLens",
                    "short_description": "Understand how ApplyLens stitches together Gmail, FastAPI, Elasticsearch, and the web UI.",
                    "detailed_description": "In this quest, you will read through the ApplyLens overview and architecture docs and answer a few code-level questions.\\n\\nBy the end you should be able to explain:\\n- The core user journey (Inbox → Tracker → Search)\\n- The main components (web, API, DB, search index, Gmail ingest)\\n- Where the primary health/metrics endpoints live.\\n",
                    "world_id": "world-projects",
                    "difficulty": "easy",
                    "quest_kind": "reading",
                    "track_id": "project-fundamentals",
                    "order_index": 10,
                    "rubric_id": "applylens_core_tour",
                    "starting_code_path": None,
                    "base_xp_reward": 30,
                    "mastery_xp_bonus": 10,
                    "unlocks_boss_id": None,
                    "unlocks_layout_id": None,
                },
                {
                    "slug": "applylens-critical-path-inbox-to-tracker",
                    "title": "Critical Path: Inbox → Tracker",
                    "short_description": "Trace the primary user flow from a new email arriving to a structured application row in the Tracker.",
                    "detailed_description": "This quest focuses on the most important path in ApplyLens: converting a raw Gmail thread into a normalized application in the Tracker.\\n\\nYou will:\\n- Identify which FastAPI routes and workers participate in the Inbox → Tracker path.\\n- Map the data model from raw email → normalized DB rows.\\n- Add or improve one guardrail or validation on that path (e.g., idempotency, duplicate protection, or schema check).\\n",
                    "world_id": "world-projects",
                    "difficulty": "medium",
                    "quest_kind": "integration",
                    "track_id": "project-fundamentals",
                    "order_index": 20,
                    "rubric_id": "applylens_critical_path_inbox_to_tracker",
                    "starting_code_path": "apps/api/app/routers/applications.py",
                    "base_xp_reward": 50,
                    "mastery_xp_bonus": 20,
                    "unlocks_boss_id": None,
                    "unlocks_layout_id": None,
                },
            ],
        },
        {
            "track_id": "project-runtime",
            "label": "Runtime & Reliability",
            "order_index": 20,
            "quests": [
                {
                    "slug": "applylens-ingest-path",
                    "title": "Ingest Path: Gmail → DB → Search",
                    "short_description": "Map and validate the ingestion pipeline that brings Gmail threads into Postgres and Elasticsearch.",
                    "detailed_description": "ApplyLens lives or dies by its ingest path.\\n\\nIn this quest, you will:\\n- Trace the full flow from a Gmail backfill or webhook to a stored email thread.\\n- Identify where the indexing into Elasticsearch happens.\\n- Add or verify at least one metric or structured log line along this path (e.g., ingest latency, index errors).\\n",
                    "world_id": "world-projects",
                    "difficulty": "medium",
                    "quest_kind": "integration",
                    "track_id": "project-runtime",
                    "order_index": 10,
                    "rubric_id": "applylens_ingest_path",
                    "starting_code_path": "apps/api/app/routers/gmail_backfill.py",
                    "base_xp_reward": 60,
                    "mastery_xp_bonus": 25,
                    "unlocks_boss_id": None,
                    "unlocks_layout_id": None,
                },
                {
                    "slug": "applylens-runtime-hardening",
                    "title": "Runtime Hardening: Spikes, Failures, Retries",
                    "short_description": "Harden ApplyLens against ingest spikes and flaky dependencies before facing The Inbox Maelstrom.",
                    "detailed_description": "This is your boss-prep quest for ApplyLens runtime.\\n\\nYou will:\\n- Review how Gmail ingest workers handle errors and retries.\\n- Ensure timeouts, retries, and backoff are configured sensibly for Gmail and Elasticsearch.\\n- Expose or validate runtime metrics (e.g., error rates, retry counts, latency histograms) that The Inbox Maelstrom will test.\\n",
                    "world_id": "world-projects",
                    "difficulty": "hard",
                    "quest_kind": "integration",
                    "track_id": "project-runtime",
                    "order_index": 20,
                    "rubric_id": "applylens_runtime_hardening",
                    "starting_code_path": "apps/api/app/workers/gmail_ingest_worker.py",
                    "base_xp_reward": 80,
                    "mastery_xp_bonus": 35,
                    "unlocks_boss_id": "applylens-runtime-boss",
                    "unlocks_layout_id": None,
                },
            ],
        },
        {
            "track_id": "project-intelligence",
            "label": "Agents & Intelligence",
            "order_index": 30,
            "quests": [
                {
                    "slug": "applylens-agent-tour",
                    "title": "Agent Tour: Inbox Triage Assistant",
                    "short_description": "Understand how the ApplyLens agent(s) read emails, classify intent, and suggest actions.",
                    "detailed_description": "In this quest you will perform a guided tour of the ApplyLens agent layer.\\n\\nYou will:\\n- Identify where the triage agent is configured (tools, prompts, models).\\n- Understand how it reads email threads and produces suggestions.\\n- Document the safety and cost guardrails that are in place (or note where they are missing).\\n",
                    "world_id": "world-projects",
                    "difficulty": "medium",
                    "quest_kind": "reading",
                    "track_id": "project-intelligence",
                    "order_index": 10,
                    "rubric_id": "applylens_agent_tour",
                    "starting_code_path": "apps/api/app/agents/inbox_triage_agent.py",
                    "base_xp_reward": 50,
                    "mastery_xp_bonus": 20,
                    "unlocks_boss_id": None,
                    "unlocks_layout_id": None,
                },
                {
                    "slug": "applylens-agent-eval-loop",
                    "title": "Agent Eval Loop: Judge & Coach",
                    "short_description": "Wire the ApplyLens triage agent into an evaluation loop so it learns from past decisions.",
                    "detailed_description": "This quest prepares you for the agent boss.\\n\\nYou will:\\n- Implement or refine an evaluation harness for the triage agent (Judge/Coach pair).\\n- Define a small benchmark of example email threads with expected classifications or actions.\\n- Emit structured eval results (scores, failure modes) that The Intent Oracle boss will use.\\n",
                    "world_id": "world-projects",
                    "difficulty": "hard",
                    "quest_kind": "integration",
                    "track_id": "project-intelligence",
                    "order_index": 20,
                    "rubric_id": "applylens_agent_eval_loop",
                    "starting_code_path": "apps/api/app/evals/agent_eval_runner.py",
                    "base_xp_reward": 80,
                    "mastery_xp_bonus": 35,
                    "unlocks_boss_id": "applylens-agent-boss",
                    "unlocks_layout_id": None,
                },
            ],
        },
    ],
    "bosses": [
        {
            "slug": "applylens-runtime-boss",
            "name": "The Inbox Maelstrom",
            "world_id": "world-projects",
            "project_slug": "applylens",
            "tech_focus": ["fastapi", "gmail", "elasticsearch", "worker", "metrics"],
            "technical_objective": "Given a surge of Gmail messages and threads, keep ingest latency under the configured SLO and error rate under 1% while maintaining a healthy Elasticsearch index.",
            "starting_code_path": "apps/api/app/workers/gmail_ingest_worker.py",
            "rubric_id": "applylens_runtime_boss",
            "hint_codex_id": "boss-applylens-runtime-strategy",
            "phase": "runtime",
            "base_hp": 100,
        },
        {
            "slug": "applylens-agent-boss",
            "name": "The Intent Oracle",
            "world_id": "world-projects",
            "project_slug": "applylens",
            "tech_focus": ["agents", "llm", "evals", "tooling"],
            "technical_objective": "Given noisy email threads, plan and execute multi-step actions (classify intent, suggest follow-ups) using tools while respecting safety and budget constraints, achieving a high eval score on the benchmark set.",
            "starting_code_path": "apps/api/app/agents/inbox_triage_agent.py",
            "rubric_id": "applylens_agent_boss",
            "hint_codex_id": "boss-applylens-agent-strategy",
            "phase": "intelligence",
            "base_hp": 120,
        },
    ],
}


def generate_project_questline(db: Session, project: Project) -> ProjectQuestlineSpec:
    """
    Generate a project-specific questline using QuestMaster agent.
    Falls back to golden spec for ApplyLens if enabled.
    """
    # Golden shortcut for ApplyLens while iterating
    use_golden = os.getenv("QUESTMASTER_GOLDEN_APPLYLENS", "0") == "1"
    if use_golden and project.slug == "applylens":
        return ProjectQuestlineSpec.parse_obj(APPLYLENS_QUESTLINE_GOLDEN)

    # TODO: Implement LLM-based generation for other projects
    # For now, only ApplyLens is supported via golden spec
    raise NotImplementedError(
        f"QuestMaster LLM generation not yet implemented. "
        f"Set QUESTMASTER_GOLDEN_APPLYLENS=1 to use golden spec for ApplyLens."
    )
