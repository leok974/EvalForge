# arcade_app/practice_gauntlet.py
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, List, Literal, Optional, Sequence

from pydantic import BaseModel, Field


PracticeItemType = Literal[
    "quest_review",
    "boss_review",
    "project_maintenance",
]


@dataclass(frozen=True)
class PracticeCandidate:
    """
    Aggregated view of something the player can practice.

    You build these from QuestRun/BossRun/Project QA, then feed them into
    build_practice_round_from_candidates.
    """

    item_type: PracticeItemType
    identifier: str  # quest_id, boss_slug, or project_slug

    # World/project context
    world_slug: Optional[str] = None  # e.g. "world-python"
    project_slug: Optional[str] = None  # e.g. "applylens"

    # Player history
    struggle_score: int = 0  # 0-100 heuristic
    attempts: int = 0
    last_run_at: Optional[datetime] = None

    # UI-friendly labels
    label: str = ""
    description: str = ""


class PracticeItemView(BaseModel):
    """
    What the UI/agent sees for a single practice item.
    """

    id: str  # derived from item_type+identifier, stable for a given candidate
    item_type: PracticeItemType
    label: str
    description: str
    world_slug: Optional[str] = None
    project_slug: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"]
    rationale: str
    struggle_score: int


class DailyPracticePlan(BaseModel):
    """
    The daily "Practice Gauntlet" plan for a player.
    """

    date: date
    label: str = "Practice Gauntlet"
    items: List[PracticeItemView] = Field(default_factory=list)
    completed_count: int = 0
    total_count: int = 0
    today_quests_completed: int = 0
    today_bosses_cleared: int = 0

    @property
    def today_trials_completed(self) -> int:
        return self.today_quests_completed + self.today_bosses_cleared
# Optional: streak_days can be filled in by a higher-level service
    streak_days: Optional[int] = None


# -----------------------
# Helpers
# -----------------------

async def get_daily_completion_stats(
    session: "AsyncSession", profile: "Profile"
) -> tuple[int, int]:
    """Return (quests_completed_today, bosses_cleared_today).

    This is defensive: if the schema isn't what we expect, we log and return zeros
    instead of throwing a 500.
    """
    from datetime import datetime, time, timedelta, timezone
    from sqlmodel import select, func, or_
    import logging
    # Import actual models found in models.py
    from arcade_app.models import QuestProgress, BossRun, QuestState

    logger = logging.getLogger(__name__)

    now = datetime.now(timezone.utc)
    start_of_day = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)

    quests_completed_today = 0
    bosses_cleared_today = 0

    # 🔢 Quests (using QuestProgress via completed_at)
    try:
        q_stmt = (
            select(func.count())
            .select_from(QuestProgress)
            .where(
                QuestProgress.user_id == profile.user_id, # Link via user_id
                QuestProgress.completed_at >= start_of_day,
                QuestProgress.completed_at < end_of_day,
            )
        )
        quests_completed_today = int((await session.exec(q_stmt)).one() or 0)
    except Exception:
        logger.exception("Practice Gauntlet: failed to compute quests_completed_today")

    # 🔢 Bosses (using BossRun via completed_at + result)
    try:
        b_stmt = (
            select(func.count())
            .select_from(BossRun)
            .where(
                BossRun.user_id == profile.user_id, # Link via user_id
                BossRun.completed_at >= start_of_day,
                BossRun.completed_at < end_of_day,
                BossRun.result == "win",
            )
        )
        bosses_cleared_today = int((await session.exec(b_stmt)).one() or 0)
    except Exception:
        logger.exception("Practice Gauntlet: failed to compute bosses_cleared_today")

    return quests_completed_today, bosses_cleared_today


# -----------------------
# Core selection utilities
# -----------------------


def stable_seed_for_profile_date(profile_id: str, for_date: date) -> int:
    """
    Produce a deterministic integer seed from (profile_id, date).

    This ensures the same player & date always get the same Practice Gauntlet,
    even if we use randomness internally.
    """
    raw = f"{profile_id}:{for_date.isoformat()}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    # Use first 16 hex chars -> 64 bits of entropy, which is plenty for seeding
    return int(digest[:16], 16)


def _dedupe_candidates(candidates: Sequence[PracticeCandidate]) -> List[PracticeCandidate]:
    """
    Deduplicate by (item_type, identifier), keeping the highest struggle_score.
    """
    best: dict[tuple[PracticeItemType, str], PracticeCandidate] = {}
    for c in candidates:
        key = (c.item_type, c.identifier)
        existing = best.get(key)
        if existing is None or c.struggle_score > existing.struggle_score:
            best[key] = c
    return list(best.values())


def _pick_with_priority(
    candidates: List[PracticeCandidate],
    n: int,
    rng: random.Random,
) -> List[PracticeCandidate]:
    """
    Pick up to n candidates, preferring higher struggle_score but with
    deterministic tie-breaking via RNG.

    Strategy:
    - Sort by struggle_score desc
    - Group by score and shuffle within each score bucket
    - Walk buckets in order until we have n
    """
    if not candidates or n <= 0:
        return []

    # Sort by struggle_score desc
    sorted_cands = sorted(candidates, key=lambda c: c.struggle_score, reverse=True)

    # Bucket by score
    buckets: dict[int, List[PracticeCandidate]] = {}
    for c in sorted_cands:
        buckets.setdefault(c.struggle_score, []).append(c)

    picked: List[PracticeCandidate] = []
    for score in sorted(buckets.keys(), reverse=True):
        bucket = buckets[score][:]
        rng.shuffle(bucket)
        for c in bucket:
            if len(picked) >= n:
                break
            picked.append(c)
        if len(picked) >= n:
            break

    return picked


def _difficulty_from_struggle(score: int) -> Literal["easy", "medium", "hard"]:
    """
    Simple mapping of struggle_score to a difficulty tag.

    You can tune this later; for now:
    - 0-39: easy
    - 40-69: medium
    - 70-100: hard
    """
    if score >= 70:
        return "hard"
    if score >= 40:
        return "medium"
    return "easy"


def _default_rationale(c: PracticeCandidate) -> str:
    """
    Generate a short, human-readable reason why this item is in the Gauntlet.
    """
    if c.attempts == 0:
        return "New challenge to expand your skills."
    if c.struggle_score >= 70:
        return "You struggled with this recently—time for a focused rematch."
    if c.struggle_score >= 40:
        return "Solid practice target to keep this skill sharp."
    return "Light warm-up to maintain familiarity."


# ----------------------------
# Main builder (pure logic)
# ----------------------------


def build_practice_round_from_candidates(
    *,
    profile_id: str,
    for_date: date,
    candidates: Sequence[PracticeCandidate],
    max_items: int = 5,
    include_worlds: Optional[set[str]] = None,
    include_projects: Optional[set[str]] = None,
    struggle_threshold: int = 60,
    maintenance_threshold: int = 20,
    rng: Optional[random.Random] = None,
) -> DailyPracticePlan:
    """
    Core Practice Gauntlet builder.

    Phase 0: This is pure logic — no DB calls, no models — so it can be tested
    in isolation. Higher-level services should:
      - Fetch Quest/Boss/Project history
      - Map them into PracticeCandidate objects
      - Call this function to get a DailyPracticePlan
      - Optionally persist PracticeRound/PracticeItem rows

    Arguments:
        profile_id: stable player identifier (stringified UUID is fine)
        for_date: the date the plan is for
        candidates: aggregated practice candidates (quests, bosses, projects)
        max_items: cap on items in the plan (default 5)
        include_worlds: if set, only candidates whose world_slug is in this set
                        (or None) are eligible
        include_projects: if set, only candidates with project_slug in this set
                          (or None) are eligible
        struggle_threshold: struggle_score >= this → struggle bucket
        maintenance_threshold: struggle_score >= this → maintenance bucket

    Returns:
        DailyPracticePlan with selected items (status/completion is not tracked here).
    """
    if max_items <= 0:
        return DailyPracticePlan(
            date=for_date,
            label="Practice Gauntlet",
            items=[],
            completed_count=0,
            total_count=0,
        )

    # Deterministic RNG
    if rng is None:
        seed = stable_seed_for_profile_date(profile_id, for_date)
        rng = random.Random(seed)

    # Filter by world / project if requested
    filtered: List[PracticeCandidate] = []
    for c in candidates:
        if include_worlds is not None and c.world_slug not in include_worlds:
            # allow project-only items with no world_slug if project is in filter
            if not (include_projects and c.project_slug in include_projects):
                continue
        if include_projects is not None and c.project_slug not in include_projects:
            # allow pure world items when world filter is set but no project filter
            if not (include_worlds and c.world_slug in include_worlds):
                continue
        filtered.append(c)

    if not filtered:
        # No matches for filters; return an empty-but-valid plan
        return DailyPracticePlan(
            date=for_date,
            label="Practice Gauntlet",
            items=[],
            completed_count=0,
            total_count=0,
        )

    # Deduplicate logically equivalent candidates
    filtered = _dedupe_candidates(filtered)

    # Partition into struggle / maintenance / exploration
    struggle: List[PracticeCandidate] = []
    maintenance: List[PracticeCandidate] = []
    exploration: List[PracticeCandidate] = []

    for c in filtered:
        if c.attempts == 0:
            exploration.append(c)
        elif c.struggle_score >= struggle_threshold:
            struggle.append(c)
        elif c.struggle_score >= maintenance_threshold:
            maintenance.append(c)
        else:
            # low struggle & has attempts: treat as light maintenance/exploration
            maintenance.append(c)

    selected: List[PracticeCandidate] = []

    # 1–2 struggle picks
    max_struggle = min(2, max_items)
    selected += _pick_with_priority(struggle, max_struggle, rng)

    # 1–2 maintenance picks
    remaining_slots = max_items - len(selected)
    if remaining_slots > 0:
        # avoid duplicates
        remaining_maintenance = [
            c for c in maintenance if c not in selected
        ]
        max_maintenance = min(2, remaining_slots)
        selected += _pick_with_priority(remaining_maintenance, max_maintenance, rng)

    # Exploration picks to fill the rest
    remaining_slots = max_items - len(selected)
    if remaining_slots > 0:
        remaining_exploration = [
            c for c in exploration if c not in selected
        ]
        # exploration is more about variety than struggle_score, so we just shuffle
        rng.shuffle(remaining_exploration)
        selected += remaining_exploration[:remaining_slots]

    # Truncate if we ever overshoot
    selected = selected[:max_items]

    # Map candidates -> PracticeItemView
    items: List[PracticeItemView] = []
    for c in selected:
        item_id = f"{c.item_type}:{c.identifier}"
        difficulty = _difficulty_from_struggle(c.struggle_score)
        rationale = _default_rationale(c)

        items.append(
            PracticeItemView(
                id=item_id,
                item_type=c.item_type,
                label=c.label or c.identifier,
                description=c.description,
                world_slug=c.world_slug,
                project_slug=c.project_slug,
                difficulty=difficulty,
                rationale=rationale,
                struggle_score=c.struggle_score,
            )
        )

    return DailyPracticePlan(
        date=for_date,
        label="Practice Gauntlet",
        items=items,
        completed_count=0,
        total_count=len(items),
    )


# --- DB-aware adapter + service layer (Phase 0: Foundry + ApplyLens) ---

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlmodel import Session
    from arcade_app.models import Profile


def _grade_to_numeric(grade: Optional[str]) -> int:
    """
    Rough numeric mapping for letter grades.
    Higher is better; used for struggle scoring.
    """
    if not grade:
        return 0
    g = grade.upper()
    mapping = {
        "S": 100,
        "A": 90,
        "B": 80,
        "C": 70,
        "D": 60,
        "F": 0,
    }
    return mapping.get(g, 0)


def _compute_struggle_score_for_boss(
    *,
    best_grade: Optional[str],
    attempts: int,
    last_run_at: Optional[datetime],
    any_autofail: bool,
) -> int:
    """
    Heuristic struggle score for bosses; more weight on autofail/low scores.
    """
    score = 0

    numeric_grade = _grade_to_numeric(best_grade)
    if any_autofail:
        score += 40
    if numeric_grade <= 60:
        score += 30
    elif numeric_grade <= 80:
        score += 15
    else:
        score += 5

    if attempts >= 3:
        score += 20
    elif attempts == 2:
        score += 10
    elif attempts == 1:
        score += 5

    return max(0, min(100, score))


async def _boss_candidates_for_profile_foundry_and_applylens(
    db: "AsyncSession",
    profile: "Profile",
) -> List[PracticeCandidate]:
    """
    Practice candidates for:
      - Foundry boss: reactor-core (world-python)
      - ApplyLens bosses: applylens-runtime-boss, applylens-agent-boss
      
    Phase 0: Uses BossDefinition table. Boss run history will be added later
    when BossRun table is implemented.
    """
    from sqlmodel import select
    from arcade_app.models import BossDefinition
    
    target_ids = {
        "reactor-core",            # Foundary boss
        "signal-prism",            # Prism boss
        "applylens-runtime-boss",  # ApplyLens runtime boss
        "applylens-agent-boss",    # ApplyLens agent boss
    }

    q_boss_defs = (
        select(BossDefinition)
        .where(BossDefinition.id.in_(target_ids))  # type: ignore
        .where(BossDefinition.enabled == True)  # type: ignore[comparison-overlap]
    )
    result = await db.execute(q_boss_defs)
    boss_defs = result.scalars().all()

    if not boss_defs:
        return []

    # TODO: Query BossRun table when it exists for real struggle scores
    # For now, create exploration candidates (attempts=0)
    candidates: List[PracticeCandidate] = []
    for boss in boss_defs:
        # Default to exploration mode until we have run history
        struggle_score = 50  # Neutral score for now
        
        candidates.append(
            PracticeCandidate(
                item_type="boss_review",
                identifier=str(boss.id),
                world_slug=boss.world_id,
                project_slug=boss.project_slug,
                struggle_score=struggle_score,
                attempts=0,  # No history yet
                last_run_at=None,
                label=boss.name,
                description=boss.description or "",
            )
        )

    return candidates


async def _quest_candidates_for_profile_foundry(
    db: "AsyncSession",
    profile: "Profile",
) -> List[PracticeCandidate]:
    """
    Build PracticeCandidate entries for Foundry (world-python) quests.
    
    Phase 0: Uses QuestDefinition table. Quest run history will be added later
    when QuestRun table is implemented.
    """
    from sqlmodel import select
    from arcade_app.models import QuestDefinition
    
    # Grab quests in world-python
    q_quests = select(QuestDefinition).where(QuestDefinition.world_id == "world-python")
    result = await db.execute(q_quests)
    quests = result.scalars().all()

    if not quests:
        return []

    # TODO: Query QuestRun table when it exists for real struggle scores
    # For now, create exploration candidates (attempts=0)
    candidates: List[PracticeCandidate] = []
    for quest in quests:
        # Default to exploration mode until we have run history
        struggle_score = 30  # Light maintenance score
        
        candidates.append(
            PracticeCandidate(
                item_type="quest_review",
                identifier=str(quest.id),
                world_slug=quest.world_id,
                project_slug=None,
                struggle_score=struggle_score,
                attempts=0,  # No history yet
                last_run_at=None,
                label=quest.title,
                description=quest.short_description or "",
            )
        )

    return candidates


def _project_maintenance_candidates_applylens(
    db: "Session",
    profile: "Profile",
) -> List[PracticeCandidate]:
    """
    Project-level maintenance items for ApplyLens.
    
    Phase 0: Simple stub that suggests running Boss QA.
    """
    return [
        PracticeCandidate(
            item_type="project_maintenance",
            identifier="applylens-daily-boss-qa",
            world_slug=None,
            project_slug="applylens",
            struggle_score=50,  # neutral; will show up in maintenance bucket
            attempts=0,
            last_run_at=None,
            label="Run ApplyLens Boss QA",
            description="Run the ApplyLens boss QA script and ensure both bosses are passing.",
        )
    ]


async def collect_practice_candidates_for_profile_foundry_applylens(
    db: "AsyncSession",
    profile: "Profile",
) -> List[PracticeCandidate]:
    """
    High-level adapter: collect all practice candidates relevant to
    Foundry (world-python) and ApplyLens.

    Phase 0: Uses definition tables only. Will be extended with run history later.
    """
    candidates: List[PracticeCandidate] = []

    candidates += await _quest_candidates_for_profile_foundry(db, profile)
    candidates += await _boss_candidates_for_profile_foundry_and_applylens(db, profile)
    candidates += _project_maintenance_candidates_applylens(db, profile)

    return candidates


async def get_daily_practice_plan_for_profile_foundry_applylens(
    db: "AsyncSession",
    profile: "Profile",
    today: date,
    max_items: int = 5,
) -> DailyPracticePlan:
    """
    Service entrypoint for Practice Gauntlet (Phase 0 scope):
      - Worlds: The Foundry (world-python)
      - Project: ApplyLens
      
    Returns a deterministic daily practice plan focused on these areas.
    """
    from datetime import datetime, time, timezone, timedelta
    from sqlmodel import select, func

    candidates = await collect_practice_candidates_for_profile_foundry_applylens(db, profile)

    plan = build_practice_round_from_candidates(
        profile_id=str(profile.id),
        for_date=today,
        candidates=candidates,
        max_items=max_items,
        include_worlds={"world-python"},
        include_projects={"applylens"},
        struggle_threshold=60,
    )

    # 🔢 NEW: Safe daily stats
    quests_today, bosses_today = await get_daily_completion_stats(db, profile)

    # Inject stats into the plan copy
    plan.today_quests_completed = quests_today
    plan.today_bosses_cleared = bosses_today
    
    return plan
