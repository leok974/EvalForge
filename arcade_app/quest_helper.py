import os
import json
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
from sqlmodel import select, desc, Session
from arcade_app.database import get_session
from arcade_app.models import QuestDefinition, QuestSource, QuestProgress, QuestState, Profile
from datetime import datetime
# Cache for worlds data
_WORLDS_CACHE = None

def _get_narrative_config(world_id: str) -> Dict:
    global _WORLDS_CACHE
    if _WORLDS_CACHE is None:
        try:
            with open("data/worlds.json", "r") as f:
                _WORLDS_CACHE = json.load(f)
        except Exception:
            _WORLDS_CACHE = []
            
    world = next((w for w in _WORLDS_CACHE if w["id"] == world_id), None)
    if world:
        return world.get("narrative_config", {})
    return {}

from arcade_app.worlds_helper import get_world

def build_quest_system_prompt(
    base_task: str,
    track_id: str,
    world_id: str | None = None,
) -> str:
    """
    Wraps the base technical task in the narrative context of the world.
    """
    world = get_world(world_id) if world_id else None
    if not world or "narrative_config" not in world:
        # Fallback – plain system prompt
        return base_task

    cfg = world["narrative_config"]
    alias = cfg.get("alias", world["name"])
    theme = cfg.get("theme", "")
    role = cfg.get("role", "Architect")
    vocab = ", ".join(cfg.get("vocabulary", []))

    return f"""
You are operating inside **{alias}** — {theme}.
The user is the **{role}** for this world.

Use the following narrative vocabulary when appropriate:
{vocab}

TASK:
{base_task}
""".strip()

async def stream_quest_generator(
    user_input: str, 
    track: Dict[str, Any],
    user_id: str = "leo" # Default for now
) -> AsyncGenerator[str, None]:
    
    # 1. Mock Check
    print(f"DEBUG: Entering stream_quest_generator for user={user_id}")
    if os.getenv("EVALFORGE_MOCK_GRADING") == "1":
        yield f"⚔️ **MOCK QUEST**\n\nObjective: Master {track.get('name')}.\nTask: {user_input}"
        return

    technical_task = ""
    source_type = track.get("source", "fundamentals")
    quest_title = "Mission"

    # --- PATH A: FUNDAMENTALS (Curriculum) ---
    if source_type == "fundamentals":
        async for session in get_session():
            # Find last completed quest order
            # We join QuestProgress -> QuestDefinition
            statement = (
                select(QuestDefinition.order_index)
                .join(QuestProgress, QuestProgress.quest_id == QuestDefinition.id)
                .where(
                    QuestProgress.user_id == user_id,
                    QuestProgress.state.in_([QuestState.COMPLETED, QuestState.MASTERED]),
                    QuestDefinition.track_id == track.get("id")
                )
                .order_by(desc(QuestDefinition.order_index))
            )
            result = await session.execute(statement)
            last_seq = result.scalars().first() or 0
            
            next_seq = last_seq + 1
            
            # Fetch Next Definition
            q_def = (await session.execute(
                select(QuestDefinition)
                .where(QuestDefinition.track_id == track.get("id"), QuestDefinition.order_index == next_seq)
            )).scalars().first()
            
            if not q_def:
                yield f"🎉 **TRACK COMPLETE**\n\nYou have mastered the {track.get('name')} curriculum. Select a new track to continue."
                return

            # Activate Quest in DB
            # Check if already active to avoid duplicates
            active_check = await session.execute(
                select(QuestProgress).where(
                    QuestProgress.user_id == user_id, 
                    QuestProgress.quest_id == q_def.id
                )
            )
            existing_qp = active_check.scalars().first()
            
            if not existing_qp:
                new_qp = QuestProgress(
                    user_id=user_id,
                    quest_id=q_def.id,
                    state=QuestState.AVAILABLE # Or IN_PROGRESS if auto-start
                )
                session.add(new_qp)
                await session.commit()
            elif existing_qp.state == QuestState.LOCKED:
                existing_qp.state = QuestState.AVAILABLE
                session.add(existing_qp)
                await session.commit()
            
            # Use detailed description if available, else short
            technical_task = q_def.detailed_description or q_def.short_description
            quest_title = q_def.title
            
    else:
        # --- PATH B: PROJECT (Dynamic) ---
        # Existing logic for repo scanning...
        repo_config = track.get("repo_config") or {}
        technical_task = f"Analyze the repo at {repo_config.get('url')} and find a refactor opportunity related to {', '.join(repo_config.get('stack', []))}."
        quest_title = "Field Operation"

    # --- SHARED: GENERATE FLAVOR TEXT ---
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
        
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)

        # Narrative Config
        world_id = track.get("world_id", "world-python")
        story = _get_narrative_config(world_id)
        
        alias = story.get("alias", "THE SYSTEM")
        role = story.get("role", "Engineer")
        theme = story.get("theme", "Standard Tech")
        vocab = ", ".join(story.get("vocabulary", []))
        analogy = story.get("analogy_prompt", "Use standard analogies.")

        prompt = f"""
        ROLE: You are {role} inside {alias}.
        THEME: {theme}
        VOCABULARY: {vocab}
        
        TASK: Present this mission to the operative.
        QUEST TITLE: {quest_title}
        TECHNICAL OBJECTIVE: {technical_task}
        
        INSTRUCTIONS:
        1. Narrative Hook: Describe the technical problem as a crisis within the theme ({theme}). 
        2. Tactical Analysis: Briefly explain the concept using this analogy: {analogy}
        3. Mission Objectives: List the *exact* technical steps from the objective.
        
        FORMAT:
        ## 📡 INCOMING TRANSMISSION: {alias}
        **Crisis Level:** CRITICAL | **Role:** {role}
        
        **Briefing:**
        [Narrative Paragraph]
        
        **Tactical Analysis:**
        [Analogy Paragraph]
        
        **Mission Objectives:**
        [Technical Steps]
        
        **Loot:** +XP
        """

        stream = await model.generate_content_async(prompt, stream=True)
        async for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\n[SYSTEM ERROR: Quest Generation Failed - {str(e)}]\n\nFallback Task: {technical_task}"

# --- QUEST SYSTEM 2.0 HELPERS ---

async def get_or_create_progress(
    session: Session, user: Profile, quest: QuestDefinition
) -> QuestProgress:
    statement = select(QuestProgress).where(
        QuestProgress.user_id == user.user_id,
        QuestProgress.quest_id == quest.id
    )
    result = await session.exec(statement)
    qp = result.first()
    if qp is None:
        qp = QuestProgress(
            user_id=user.user_id,
            quest_id=quest.id,
            state=QuestState.AVAILABLE,
        )
        session.add(qp)
        await session.flush()
        await session.refresh(qp)
    return qp


async def record_quest_submission(
    session: Session,
    user: Profile,
    quest: QuestDefinition,
    score: float,
    passed: bool,
) -> QuestProgress:
    qp = await get_or_create_progress(session, user, quest)
    qp.attempts += 1
    qp.last_submitted_at = datetime.utcnow()

    if qp.best_score is None or score > qp.best_score:
        qp.best_score = score

    # Update state machine
    if passed:
        if qp.state in (QuestState.LOCKED, QuestState.AVAILABLE):
            qp.state = QuestState.COMPLETED
            qp.completed_at = datetime.utcnow()
        elif qp.state in (QuestState.IN_PROGRESS, QuestState.COMPLETED):
            qp.state = QuestState.MASTERED
            qp.mastered_at = datetime.utcnow()
    else:
        # On failure we at least mark it as in_progress
        if qp.state == QuestState.AVAILABLE:
            qp.state = QuestState.IN_PROGRESS

    session.add(qp)
    await session.commit()
    await session.refresh(qp)
    return qp


def quest_to_dict(q: QuestDefinition, state: Optional[QuestProgress]) -> Dict[str, Any]:
    ps = state.state if state else QuestState.LOCKED
    return {
        "id": q.id,
        "slug": q.slug,
        "world_id": q.world_id,
        "track_id": q.track_id,
        "order_index": q.order_index,
        "title": q.title,
        "short_description": q.short_description,
        "state": ps.value,
        "best_score": state.best_score if state else None,
        "attempts": state.attempts if state else 0,
        "unlocks_boss_id": q.unlocks_boss_id,
        "unlocks_layout_id": q.unlocks_layout_id,
        "base_xp_reward": q.base_xp_reward,
        "mastery_xp_bonus": q.mastery_xp_bonus,
    }

def _ensure_flags_dict(user: Profile):
  if user.flags is None:
      user.flags = {}
  if not isinstance(user.flags, dict):
      user.flags = dict(user.flags)

def apply_quest_unlocks(
    session: Session,
    user: Profile,
    quest: QuestDefinition,
    prev_state: QuestState | None,
    new_state: QuestState,
) -> list[dict]:
    """
    If this submission transitions the quest into COMPLETED/MASTERED
    for the first time, unlock any boss/layout attached to it.

    Returns a list of unlock_events for the API response.
    """
    unlock_events: list[dict] = []

    # Only fire unlocks on the first time we "complete" this quest line.
    just_completed = (
        prev_state not in (QuestState.COMPLETED, QuestState.MASTERED)
        and new_state in (QuestState.COMPLETED, QuestState.MASTERED)
    )

    if not just_completed:
        return unlock_events

    _ensure_flags_dict(user)

    # Layout unlock
    if quest.unlocks_layout_id:
        # Create a copy to ensure change tracking
        current_flags = dict(user.flags) if user.flags else {}
        layouts = set(current_flags.get("layouts_unlocked", []))
        
        if quest.unlocks_layout_id not in layouts:
            layouts.add(quest.unlocks_layout_id)
            current_flags["layouts_unlocked"] = sorted(layouts)
            user.flags = current_flags # Re-assign to trigger update
            
            unlock_events.append(
                {
                    "type": "layout",
                    "id": quest.unlocks_layout_id,
                    "label": quest.unlocks_layout_id,
                }
            )

    # Boss unlock
    if quest.unlocks_boss_id:
        # Create a copy to ensure change tracking (refresh from object in case layout update changed it)
        current_flags = dict(user.flags) if user.flags else {}
        bosses = set(current_flags.get("bosses_unlocked", []))
        
        if quest.unlocks_boss_id not in bosses:
            bosses.add(quest.unlocks_boss_id)
            current_flags["bosses_unlocked"] = sorted(bosses)
            user.flags = current_flags # Re-assign to trigger update
            
            unlock_events.append(
                {
                    "type": "boss",
                    "id": quest.unlocks_boss_id,
                    "label": quest.unlocks_boss_id,
                }
            )

    if unlock_events:
        session.add(user)

    return unlock_events
