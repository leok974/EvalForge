from collections import defaultdict
from typing import List, Dict

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from arcade_app.models import QuestDefinition, QuestProgress, QuestState, TrackDefinition

class TrackProgressRow(dict):
    """Simple dict row for JSON output."""
    # keys: world_slug, track_slug, label, progress, total_quests, completed_quests

async def compute_track_progress_for_user(
    db: AsyncSession,
    user_id: str,
) -> List[TrackProgressRow]:
    # 1. Fetch all quest definitions
    quest_defs = (await db.exec(select(QuestDefinition))).all()
    if not quest_defs:
        return []

    # 2. Fetch all tracks to get labels (optional but good for UI)
    track_defs = (await db.exec(select(TrackDefinition))).all()
    track_labels = {t.id: t.name for t in track_defs}

    # 3. Fetch all completed/mastered quest progress for this user
    # Note: State is Enum.
    completed_runs = (
        await db.exec(
            select(QuestProgress).where(
                QuestProgress.user_id == user_id,
                QuestProgress.state.in_([QuestState.COMPLETED, QuestState.MASTERED])
            )
        )
    ).all()

    completed_quest_ids = {run.quest_id for run in completed_runs}

    # 4. Group quests by (world_id, track_id)
    total_by_track: Dict[tuple[str, str], int] = defaultdict(int)
    completed_by_track: Dict[tuple[str, str], int] = defaultdict(int)
    
    # We also need to know which tracks exist even if they have 0 quests (though rare)
    # But usually we iterate quests to find populated tracks.
    
    known_tracks = set()

    for q in quest_defs:
        key = (q.world_id, q.track_id)
        total_by_track[key] += 1
        known_tracks.add(key)

        if q.id in completed_quest_ids:
            completed_by_track[key] += 1

    # 5. Build rows
    rows: List[TrackProgressRow] = []
    for key in known_tracks:
        world_id, track_id = key
        total = total_by_track[key]
        completed = completed_by_track.get(key, 0)
        
        if total <= 0:
            progress_percent = 0.0
        else:
            progress_percent = round((completed / total) * 100.0, 1)

        # Get label from TrackDefinition or fallback to slug
        label = track_labels.get(track_id, track_id)

        rows.append(
            TrackProgressRow(
                world_slug=world_id, # Using ID as slug
                track_slug=track_id,
                label=label,
                progress=progress_percent,
                total_quests=total,
                completed_quests=completed,
            )
        )

    # Sort for deterministic output
    rows.sort(key=lambda r: (r["world_slug"], r["track_slug"]))
    return rows
