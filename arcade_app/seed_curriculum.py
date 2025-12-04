from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from arcade_app.database import engine
from arcade_app.models import QuestDefinition, TrackDefinition

_ORACLE_INVOCATION_STARTING_CODE = r"""\"\"\"Oracle Quest 1 – Invocation

Goal:
- Implement `plan_actions_basic(goal, tools)` that chooses 1–2 steps
  for simple inspect or modify goals.

Differences from the boss:
- No dangerous / unsafe inputs in this quest.
- No need for complex goal classification.
- Focus is on structure and picking *relevant* allowed tools.

Each step must include:
- 'tool': tool name (string)
- 'input': dict of arguments
- 'reason': short string explaining why this step exists.
\"\"\"

from typing import Any, Dict, List, TypedDict


class ToolSpec(TypedDict, total=False):
    name: str
    description: str
    allowed: bool
    kind: str  # "read" | "write" | "message"
    input_schema: Dict[str, Any]


class PlanStep(TypedDict, total=False):
    tool: str
    input: Dict[str, Any]
    reason: str


def plan_actions_basic(goal: str, tools: List[ToolSpec]) -> List[PlanStep]:
    \"\"\"Return a simple plan for a safe goal.

    Rules:
    - Use only tools with allowed == True.
    - Prefer read tools first, then write tools, if applicable.
    - For very simple 'show/list/get' goals, a single read step is enough.
    - If no useful tool exists, return a single 'none' step explaining why.
    \"\"\"
    # TODO: Implement a real basic planner.
    return [
        {
            "tool": "none",
            "input": {},
            "reason": "Planner not implemented yet.",
        }
    ]
"""

_ORACLE_INVOCATION_RUBRIC = """
Scoring (0–100):

Structure (0-30 pts)
- Returns a list of steps; each step has tool, input, reason.

Allowed Tools Only (0-25 pts)
- Never uses tools where allowed == False.

Basic Relevance (0-25 pts)
- Picks read tools for 'show/list/get' goals; uses write tools only when the goal clearly implies a change.

Fallback Behavior (0-20 pts)
- When no suitable tool exists, returns a 'none' plan with a clear explanation.
"""

_ORACLE_GROUNDING_STARTING_CODE = r"""\"\"\"Oracle Quest 2 – Grounding

Goal:
- Extend basic planning with *safety awareness*:
  - Detect obviously unsafe / destructive goals.
  - Refuse them by returning a 'none' step with a clear reason.
  - For safe goals, emit a small READ → optional MESSAGE → WRITE plan.

This is a smaller version of the Intent Oracle boss planner.

Use:
- 'dangerous' keywords to trigger refusal.
- allowed tools only.
\"\"\"

from typing import Any, Dict, List, TypedDict


class ToolSpec(TypedDict, total=False):
    name: str
    description: str
    allowed: bool
    kind: str    # "read" | "write" | "message"
    input_schema: Dict[str, Any]


class PlanStep(TypedDict, total=False):
    tool: str
    input: Dict[str, Any]
    reason: str


def _classify_goal(goal: str) -> str:
    g = goal.lower()
    if any(x in g for x in ["delete database", "drop table", "wipe logs", "destroy"]):
        return "dangerous"
    if any(x in g for x in ["configure", "update", "change", "create", "enable", "disable"]):
        return "modify"
    if any(x in g for x in ["show", "list", "fetch", "get", "inspect", "status"]):
        return "inspect"
    return "generic"


def plan_actions_grounded(goal: str, tools: List[ToolSpec]) -> List[PlanStep]:
    \"\"\"Return a safety-aware plan.

    Rules:
    - For dangerous goals: return 'none' with a refusal reason.
    - For inspect/modify goals:
      - Use allowed read tools to inspect.
      - Optionally log via message tool.
      - Use write tool only when needed.
    - If no safe plan exists: 'none' + explanation.
    \"\"\"
    # TODO: Implement; currently always refuses.
    return [
        {
            "tool": "none",
            "input": {},
            "reason": "Planner not implemented yet (Grounding quest).",
        }
    ]
"""

_ORACLE_GROUNDING_RUBRIC = """
Scoring (0–100):

Dangerous Refusal (0-30 pts)
- Correctly detects clearly dangerous goals and refuses with tool='none' and a clear reason.

Safe Planning (0-30 pts)
- For safe goals, uses allowed tools and emits multi-step plans where appropriate (inspect → write).

Ordering (0-20 pts)
- Prefers READ before WRITE; optional message/log step is placed sensibly.

Fallback Behavior (0-20 pts)
- Provides an explanatory 'none' plan when no safe actions are possible.
"""

async def seed_oracle_curriculum():
    print("🌱 Seeding Oracle Curriculum...")
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        # 1. Track
        track_slug = "oracle-fundamentals"
        stmt = select(TrackDefinition).where(TrackDefinition.id == track_slug)
        existing_track = (await session.execute(stmt)).scalar_one_or_none()
        
        if not existing_track:
            print(f"  - Creating Track: {track_slug}")
            track = TrackDefinition(
                id=track_slug, # Using id as slug for simplicity if model supports it, or check model
                # Assuming TrackDefinition has id, name, description, world_id
                world_id="world-oracle",
                name="Invocation & Grounding",
                description="Learn to design safe, structured plans for tool-based agents.",
                # order_index=0, # If model has this
            )
            session.add(track)
        
        # 2. Quests
        quests = [
            {
                "id": "oracle-invocation",
                "name": "Invocation",
                "summary": "Turn simple goals into one- or two-step plans with allowed tools.",
                "tech_obj": (
                    "Implement a basic planner that selects appropriate tools for simple inspect/modify goals, "
                    "ensuring each step has tool, input, and reason fields."
                ),
                "starting_code": _ORACLE_INVOCATION_STARTING_CODE,
                "rubric": _ORACLE_INVOCATION_RUBRIC,
                "xp": 100,
                "order": 0,
                "prereq": None
            },
            {
                "id": "oracle-grounding",
                "name": "Grounding",
                "summary": "Respect safety constraints and refuse unsafe intents with clear explanations.",
                "tech_obj": (
                    "Extend the planner to classify goals, handle unsafe requests, and emit safe refusal plans "
                    "when required, while still planning multi-step READ → THINK → WRITE flows for safe goals."
                ),
                "starting_code": _ORACLE_GROUNDING_STARTING_CODE,
                "rubric": _ORACLE_GROUNDING_RUBRIC,
                "xp": 150,
                "order": 1,
                "prereq": "oracle-invocation"
            }
        ]

        for q in quests:
            stmt = select(QuestDefinition).where(QuestDefinition.id == q["id"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            
            if not existing:
                print(f"  - Creating Quest: {q['id']}")
                quest = QuestDefinition(
                    id=q["id"],
                    track_id=track_slug,
                    title=q["name"], # Model uses title
                    technical_objective=q["tech_obj"],
                    rubric_hints=q["rubric"],
                    xp_reward=q["xp"],
                    sequence_order=q["order"],
                    # prerequisite_slug=q["prereq"], # If model supports it
                    boss=False
                )
                session.add(quest)
            else:
                print(f"  - Updating Quest: {q['id']}")
                existing.technical_objective = q["tech_obj"]
                existing.rubric_hints = q["rubric"]
                existing.title = q["name"]
                session.add(existing)

        await session.commit()
    print("✅ Oracle Curriculum Seeded.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_oracle_curriculum())
