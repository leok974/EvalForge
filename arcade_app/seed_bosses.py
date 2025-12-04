from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from arcade_app.models import BossDefinition, KnowledgeChunk
from arcade_app import database

REACTOR_STARTING_CODE = """# reactor.py
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/reactor/status")
def reactor_status():
    # Simulate slow blocking I/O
    time.sleep(3)
    return {"status": "stable", "temperature": 900}
"""

REACTOR_RUBRIC = """
Scoring (0–100):

Async correctness (0–40 pts)
- async def on the route (10)
- At least one await in the function body (10)
- No time.sleep anywhere (10)
- Uses asyncio.sleep or equivalent (10)

Model & typing (0–30 pts)
- ReactorStatus model present, subclass of BaseModel (10)
- Has fields status: str and temperature: int (10)
- Route annotated to return ReactorStatus and/or uses response_model (10)

Structure & clarity (0–20 pts)
- Helper async def fetch_reactor_status() exists (10)
- Endpoint uses helper instead of inlining everything (5)
- No obvious junk / debug prints / unused imports (5)

Style & extras (0–10 pts)
- Good naming, docstring, or small extra (e.g. handling delay as a param).
"""

_SIGNAL_PRISM_STARTING_CODE_TS = r"""// Prism Boss: The Signal Prism
// World: JS / TypeScript
//
// You are given a stream of events that arrive in (mostly) ascending timestamp order,
// but you MUST NOT assume they are perfectly ordered or unique.
//
// Your job: implement `computeSignalPanel` as a pure function that transforms an
// array of events into the final panel state.
//
// Rules (summarized, see full spec in the boss prompt):
// - Events refer to signals by `id`.
// - `open` creates or reopens a signal.
// - `update` mutates severity/message on an existing signal.
// - `close` marks a signal as closed.
// - `ack` marks a signal as acknowledged (but may remain visible).
// - Later events with a higher `ts` win over earlier ones for that signal.
// - Duplicate events (same id/kind/ts) must not cause duplicate signals.
//
// Hints:
// - Think in terms of a reducer over a Map<string, SignalState>.
// - Make the function pure & deterministic: no mutation of input array,
//   no random calls, no time-based behavior.

export type Channel = "ui" | "network" | "system";

export type Severity = "info" | "warn" | "error";

export type SignalEvent = {
  id: string;
  channel: Channel;
  kind: "open" | "update" | "close" | "ack";
  ts: number; // unix ms
  payload?: {
    severity?: Severity;
    message?: string;
  };
};

export type SignalState = {
  id: string;
  channel: Channel;
  severity: Severity;
  message: string;
  open: boolean;
  acknowledged: boolean;
  lastEventAt: number;
};

export function computeSignalPanel(events: SignalEvent[]): SignalState[] {
  // TODO: implement
  // Requirements:
  // - Must be pure (no reliance on external mutable state).
  // - Must treat events as a set: later ts wins, duplicates are safe.
  // - Must return a stable array of SignalState (order may be defined by id or ts).
  return [];
}
"""

_SIGNAL_PRISM_RUBRIC = """
Scoring (0–100):

Correctness (0-40 pts)
- Produces expected SignalState[] for variety of streams (10)
- Handles out-of-order events correctly (later ts wins) (10)
- Handles duplicates correctly (idempotent) (10)
- Handles partial payloads (merges instead of overwrites) (10)

Design Purity (0-30 pts)
- Pure function, no external state mutation (10)
- Uses Map<string, SignalState> or equivalent efficient structure (10)
- Returns stable array (e.g. sorted by ID) (10)

Edge Cases (0-20 pts)
- Handles empty arrays gracefully (5)
- Handles unknown kinds or missing fields gracefully (5)
- Handles channel switching consistent with strategy (5)
- Handles repeated closes/acks gracefully (5)

Performance (0-10 pts)
- Reasonable time/space complexity (no O(n^2) in hot paths) (10)
"""

_INTENT_ORACLE_STARTING_CODE = r"""\"\"\"Intent Oracle Boss – Planner Stub

You are given:
- a natural language goal (string)
- a list of tools with their capabilities & safety info

Your job:
- Implement `plan_actions(goal, tools)` as a PURE function that returns
  a *plan* – an ordered list of steps the agent should take.

Each step MUST be a dict with:
- 'tool': name of the tool to call (string)
- 'input': dict of arguments for that tool
- 'reason': short natural-language justification

Rules:
- Only use tools that are marked `allowed: True`.
- Respect constraints implied in the goal (no forbidden / unsafe actions).
- Prefer a READ -> THINK -> WRITE sequence when possible:
    1) Inspect / fetch state with read-only tools.
    2) Decide / refine based on that.
    3) Apply mutations / side-effects only at the end.

If no safe plan exists, return a single-step plan with:
- tool: "none"
- input: {}
- reason: explanation why the request cannot be safely executed.

You do NOT execute tools here. You only plan.

See docstring on `plan_actions` for more details.
\"\"\"


from typing import Any, Dict, List, TypedDict


class ToolSpec(TypedDict, total=False):
    name: str
    description: str
    allowed: bool
    kind: str  # e.g. "read", "write", "message"
    input_schema: Dict[str, Any]


class PlanStep(TypedDict, total=False):
    tool: str
    input: Dict[str, Any]
    reason: str


def plan_actions(goal: str, tools: List[ToolSpec]) -> List[PlanStep]:
    \"\"\"Return a safe, structured plan for the given goal.

    Parameters
    ----------
    goal:
        Natural language description of what the user wants.
    tools:
        List of available tools. Each tool has:
        - name (str)
        - description (str)
        - allowed (bool)
        - kind (\"read\" | \"write\" | \"message\" | ...)
        - input_schema (free-form schema, may be partial)

    Returns
    -------
    List[PlanStep]
        Ordered list of steps. Each step MUST have:
        - tool (str)
        - input (dict)
        - reason (short string)

    Rules
    -----
    - Never use tools with allowed == False.
    - Prefer:
        1) read-only tools first (kind == \"read\")
        2) then write tools (kind == \"write\"), if needed.
    - If the goal is unsafe or impossible with the given tools,
      return a single step with tool=\"none\" and a clear explanation.
    \"\"\"
    # TODO: Implement a real planner.
    # For now, return a trivial no-op plan that just explains we did nothing.
    return [
        {
            \"tool\": \"none\",
            \"input\": {},
            \"reason\": \"Planner not yet implemented. No actions taken.\",
        }
    ]
"""

_INTENT_ORACLE_RUBRIC = """
Scoring (0–100):

Structure (0-25 pts)
- Plan is a list of steps with valid tool, input, and reason fields (25)

Tool Selection (0-25 pts)
- Chooses only allowed tools and picks tools that are relevant to the goal (25)

Safety & Constraints (0-20 pts)
- Avoids unsafe tools when the goal is dangerous or out-of-scope; returns a safe refusal plan when needed (20)

Goal Coverage (0-20 pts)
- Steps collectively address the goal from start to finish (not just one sub-piece) (20)

Ordering & Efficiency (0-10 pts)
- Plan follows a sensible READ → THINK → WRITE ordering and avoids unnecessary tool calls (10)
"""

async def seed_bosses():
    print("Seeding Bosses...")
    async_session = sessionmaker(
        database.engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # ... (Reactor Core and Signal Prism seeding remains the same) ...
        # 1. Reactor Core
        boss_id = "boss-reactor-core"
        stmt = select(BossDefinition).where(BossDefinition.id == boss_id)
        existing = (await session.execute(stmt)).scalar_one_or_none()

        if not existing:
            print(f"  - Creating {boss_id}")
            boss = BossDefinition(
                id=boss_id,
                name="The Reactor Core",
                description="A high-pressure backend service that demands async correctness and robust error handling.",
                # technical_objective="Implement a stable reactor status endpoint that handles high load without blocking.",
                rubric=REACTOR_RUBRIC,
                world_id="world-python",
                track_id="backend-api",
                time_limit_seconds=1800,
                max_hp=100,
                difficulty="hard",
                hint_codex_id="boss-reactor-core-strategy", # Linked Strategy Guide
                enabled=True
            )
            session.add(boss)
        else:
            print(f"  - Updating {boss_id}")
            existing.hint_codex_id = "boss-reactor-core-strategy"
            # existing.technical_objective = "Implement a stable reactor status endpoint that handles high load without blocking."
            existing.rubric = REACTOR_RUBRIC
            session.add(existing)
        
        # 2. Signal Prism
        boss_id_prism = "signal_prism"
        stmt_prism = select(BossDefinition).where(BossDefinition.id == boss_id_prism)
        existing_prism = (await session.execute(stmt_prism)).scalar_one_or_none()

        if not existing_prism:
            print(f"  - Creating {boss_id_prism}")
            boss_prism = BossDefinition(
                id=boss_id_prism,
                name="The Signal Prism",
                description="Fold a chaotic event stream into a stable Signal Panel state. Tests JS/TS reducers, event ordering, and consistent state shapes.",
                # technical_objective="Implement a pure, deterministic TypeScript reducer that takes an array of SignalEvent objects and returns the final SignalState[] for a panel.",
                rubric=_SIGNAL_PRISM_RUBRIC,
                world_id="world-prism",
                track_id="prism-fundamentals",
                time_limit_seconds=2400,
                max_hp=150,
                difficulty="hard",
                hint_codex_id="boss-signal-prism-strategy",
                enabled=True,
                starting_code=_SIGNAL_PRISM_STARTING_CODE_TS
            )
            session.add(boss_prism)
        else:
            print(f"  - Updating {boss_id_prism}")
            existing_prism.hint_codex_id = "boss-signal-prism-strategy"
            # existing_prism.technical_objective = "Implement a pure, deterministic TypeScript reducer that takes an array of SignalEvent objects and returns the final SignalState[] for a panel."
            existing_prism.rubric = _SIGNAL_PRISM_RUBRIC
            existing_prism.starting_code = _SIGNAL_PRISM_STARTING_CODE_TS
            session.add(existing_prism)

        await session.commit()

        # 3. Seed Codex Docs
        print("  - Seeding Codex Docs...")
        
        # Reactor Core Docs
        reactor_docs = [
            {
                "tier": 1,
                "slug": "reactor-core-tier-1",
                "title": "Reactor Core: Basic Analysis",
                "content": """# Reactor Core: Basic Analysis
The reactor core is a high-throughput system.
Key observations:
- The `reactor_status` endpoint is slow.
- It uses `time.sleep(3)`, which blocks the event loop.
- This causes the server to become unresponsive under load.
"""
            },
            {
                "tier": 2,
                "slug": "reactor-core-tier-2",
                "title": "Reactor Core: Async Patterns",
                "content": """# Reactor Core: Async Patterns
To fix the blocking issue:
1. Use `async def` for the route handler.
2. Replace `time.sleep()` with `asyncio.sleep()`.
3. Ensure the return type matches the Pydantic model.
"""
            },
            {
                "tier": 3,
                "slug": "reactor-core-tier-3",
                "title": "Reactor Core: Advanced Optimization",
                "content": """# Reactor Core: Advanced Optimization
For maximum performance:
- Offload heavy computation to a thread pool if needed.
- Use caching for status if it doesn't change often.
- Add proper error handling for sensor failures.
"""
            }
        ]

        # Signal Prism Docs
        # Read content from files we just created
        def read_file(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}")
                return ""

        prism_docs = [
            {
                "tier": 1,
                "slug": "signal-prism-lore",
                "title": "The Signal Prism – System Briefing",
                "content": read_file("data/codex/bosses/signal_prism/signal-prism-lore.md")
            },
            {
                "tier": 2,
                "slug": "signal-prism-attacks",
                "title": "The Signal Prism – Attack Patterns",
                "content": read_file("data/codex/bosses/signal_prism/signal-prism-attacks.md")
            },
            {
                "tier": 3,
                "slug": "signal-prism-strategy",
                "title": "The Signal Prism – Strategy Guide",
                "content": read_file("data/codex/bosses/signal_prism/signal-prism-strategy.md")
            }
        ]
        # Ensure Signal Prism docs have boss_id set
        for d in prism_docs:
            d["boss_id"] = "signal_prism"

        # Multi-Boss Definitions
        new_bosses = [
            {
                "id": "query_vault",
                "name": "The Query Vault",
                "world_id": "world-archives",
                "track_id": "sql-analytics",
                "desc": "A locked analytics vault that only opens to precise, efficient queries.",
                "tech_obj": "Write precise, robust SQL to answer analytics questions without double-counting or ignoring NULLs.",
                "hint": "boss-query-vault-strategy",
                "docs_path": "data/codex/bosses/query_vault",
                "slug_prefix": "query-vault",
                "rubric": "Placeholder Rubric",
                "starting_code": "# TODO: Implement starting code"
            },
            {
                "id": "containment_grid",
                "name": "The Containment Grid",
                "world_id": "world-grid",
                "track_id": "infra-docker",
                "desc": "Fix a broken docker-compose stack to make services healthy and connected.",
                "tech_obj": "Configure docker-compose services, networks, and environment variables to ensure a healthy boot.",
                "hint": "boss-containment-grid-strategy",
                "docs_path": "data/codex/bosses/containment_grid",
                "slug_prefix": "containment-grid",
                "rubric": "Placeholder Rubric",
                "starting_code": "# TODO: Implement starting code"
            },
            {
                "id": "intent_oracle",
                "name": "The Intent Oracle",
                "world_id": "world-oracle",
                "track_id": "agents-planning",
                "desc": "Implement a planner that turns natural language goals into safe, structured plans.",
                "tech_obj": "Create a planner that decomposes goals into valid tool calls while respecting safety constraints.",
                "hint": "boss-intent-oracle-strategy",
                "docs_path": "data/codex/bosses/intent_oracle",
                "slug_prefix": "intent-oracle",
                "rubric": _INTENT_ORACLE_RUBRIC,
                "starting_code": _INTENT_ORACLE_STARTING_CODE
            },
            {
                "id": "branch_keeper",
                "name": "The Branch Keeper",
                "world_id": "world-timeline",
                "track_id": "git-workflow",
                "desc": "Navigate complex Git scenarios: divergent branches, conflicts, and release tagging.",
                "tech_obj": "Determine the correct sequence of Git operations to resolve conflicts and sync branches safely.",
                "hint": "boss-branch-keeper-strategy",
                "docs_path": "data/codex/bosses/branch_keeper",
                "slug_prefix": "branch-keeper",
                "rubric": "Placeholder Rubric",
                "starting_code": "# TODO: Implement starting code"
            },
            {
                "id": "gradient_nexus",
                "name": "The Gradient Nexus",
                "world_id": "world-synapse",
                "track_id": "ml-training",
                "desc": "Train a model honestly: correct splits, valid metrics, and overfitting detection.",
                "tech_obj": "Implement a training loop with proper train/val splits and metric tracking to detect overfitting.",
                "hint": "boss-gradient-nexus-strategy",
                "docs_path": "data/codex/bosses/gradient_nexus",
                "slug_prefix": "gradient-nexus",
                "rubric": "Placeholder Rubric",
                "starting_code": "# TODO: Implement starting code"
            }
        ]

        # Seed New Bosses
        for b in new_bosses:
            stmt = select(BossDefinition).where(BossDefinition.id == b["id"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            
            if not existing:
                print(f"  - Creating {b['id']}")
                boss = BossDefinition(
                    id=b["id"],
                    name=b["name"],
                    description=b["desc"],
                    # technical_objective=b["tech_obj"],
                    rubric=b["rubric"],
                    world_id=b["world_id"],
                    track_id=b["track_id"],
                    time_limit_seconds=1800,
                    max_hp=100,
                    difficulty="hard",
                    hint_codex_id=b["hint"],
                    enabled=True,
                    starting_code=b["starting_code"]
                )
                session.add(boss)
            else:
                print(f"  - Updating {b['id']}")
                existing.description = b["desc"]
                # existing.technical_objective = b["tech_obj"]
                existing.hint_codex_id = b["hint"]
                existing.rubric = b["rubric"]
                existing.starting_code = b["starting_code"]
                session.add(existing)
            
            # Prepare Docs
            b_docs = [
                {
                    "tier": 1,
                    "slug": f"boss-{b['slug_prefix']}-lore",
                    "title": f"{b['name']} – System Briefing",
                    "content": read_file(f"{b['docs_path']}/{b['slug_prefix']}-lore.md")
                },
                {
                    "tier": 2,
                    "slug": f"boss-{b['slug_prefix']}-attacks",
                    "title": f"{b['name']} – Attack Patterns",
                    "content": read_file(f"{b['docs_path']}/{b['slug_prefix']}-attacks.md")
                },
                {
                    "tier": 3,
                    "slug": f"boss-{b['slug_prefix']}-strategy",
                    "title": f"{b['name']} – Strategy Guide",
                    "content": read_file(f"{b['docs_path']}/{b['slug_prefix']}-strategy.md")
                }
            ]
            
            for d in b_docs:
                d["boss_id"] = b["id"]
                prism_docs.append(d) # Add to the list to be processed below

        all_docs = []
        for d in reactor_docs:
            d["boss_id"] = "boss-reactor-core"
            all_docs.append(d)
        
        for d in prism_docs:
            # prism_docs now contains Signal Prism + all new bosses
            all_docs.append(d)

        for doc in all_docs:
            if not doc["content"]: continue # Skip if file read failed

            stmt = select(KnowledgeChunk).where(KnowledgeChunk.source_id == doc["slug"])
            existing_chunk = (await session.execute(stmt)).scalar_one_or_none()
            
            if not existing_chunk:
                chunk = KnowledgeChunk(
                    source_type="codex",
                    source_id=doc["slug"],
                    chunk_index=0,
                    content=doc["content"],
                    embedding=[0.0]*768, # Dummy embedding
                    metadata_json={
                        "boss_id": doc["boss_id"],
                        "tier": doc["tier"],
                        "title": doc["title"]
                    }
                )
                session.add(chunk)
            else:
                existing_chunk.content = doc["content"]
                existing_chunk.metadata_json = {
                    "boss_id": doc["boss_id"],
                    "tier": doc["tier"],
                    "title": doc["title"]
                }
                session.add(existing_chunk)

        await session.commit()
    print("Bosses Seeded.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_bosses())
