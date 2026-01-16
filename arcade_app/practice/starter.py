from sqlalchemy import select, func
from arcade_app.models import QuestProgress
from arcade_app.practice.constants import STARTER_WORLD_SLUG, STARTER_QUEST_ID

async def ensure_starter_unlocked(session, profile) -> None:
    """
    If this profile has no quest progress yet, unlock the starter quest
    so the player always has something to click.
    """
    # Any progress at all? If yes, we assume progression is already in motion.
    has_progress = await session.scalar(
        select(func.count(QuestProgress.id)).where(
            QuestProgress.user_id == profile.user_id
        )
    )
    if has_progress:
        return

    # No progress: create a starter quest record
    # resolving the ID from the slug
    from arcade_app.models import QuestDefinition
    
    # 1. Get the actual integer ID for the starter quest
    q_def = await session.scalar(
        select(QuestDefinition).where(
            QuestDefinition.slug == STARTER_QUEST_ID
        )
    )
    
    if not q_def:
        # Fallback safeguard: if seed data is missing, we can't unlock it.
        # Log error or silently return? Silent is safer for production uptime.
        return

    from arcade_app.models import QuestState
    starter = QuestProgress(
        user_id=profile.user_id,
        quest_id=q_def.id,
        state=QuestState.AVAILABLE,
        attempts=0
    )
    session.add(starter)
    await session.commit()
