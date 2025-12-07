import json
import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from arcade_app.database import engine
from arcade_app.models import QuestDefinition, TrackDefinition, BossDefinition

CURRICULUM_FILE = "arcade_app/curriculum_spec.json"

def format_quest_description(q):
    """Combine rich fields into a Markdown detailed description."""
    parts = []
    if "objective" in q:
        parts.append(f"**Objective:**\n{q['objective']}")
    
    if "tasks" in q:
        task_list = "\n".join([f"- {t}" for t in q['tasks']])
        parts.append(f"**Tasks:**\n{task_list}")
        
    if "acceptance_criteria" in q:
        crit_list = "\n".join([f"- {c}" for c in q['acceptance_criteria']])
        parts.append(f"**Acceptance Criteria:**\n{crit_list}")
        
    return "\n\n".join(parts)

async def seed_expanded_curriculum():
    print("🌱 Seeding Expanded Curriculum from JSON...")
    
    if not os.path.exists(CURRICULUM_FILE):
        print(f"❌ Error: {CURRICULUM_FILE} not found.")
        return

    with open(CURRICULUM_FILE, "r") as f:
        specs = json.load(f)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        for world_spec in specs:
            world_slug = world_spec["world_slug"]
            print(f"🌍 Processing World: {world_slug}")
            
            for tier_group in world_spec.get("tier_tracks", []):
                for track_def in tier_group["tracks"]:
                    track_id = track_def["track_id"]
                    
                    # Upsert Track
                    stmt = select(TrackDefinition).where(TrackDefinition.id == track_id)
                    existing_track = (await session.execute(stmt)).scalar_one_or_none()
                    
                    boss_slug = None
                    if "boss" in track_def:
                        boss_slug = track_def["boss"]["slug"]

                    if not existing_track:
                        print(f"  - Creating Track: {track_id}")
                        track = TrackDefinition(
                            id=track_id,
                            world_id=world_slug,
                            name=track_def["title"],
                            description=f"Difficulty: {track_def.get('difficulty', 'standard')}",
                            boss_slug=boss_slug
                        )
                        session.add(track)
                    else:
                        existing_track.name = track_def["title"]
                        existing_track.boss_slug = boss_slug
                        session.add(existing_track)
                        
                    # Upsert Quests
                    for index, q in enumerate(track_def["quests"]):
                        quest_slug = q["slug"]
                        # Prepend track or world to slug if needed to ensure uniqueness?
                        # The JSON uses short slugs like 'warmup-script'.
                        # Ideally robust ID is best. The JSON has 'quest_id' (e.g. "py-ignition-q1-warmup-script").
                        # We should use 'quest_id' if available as the unique slug.
                        db_quest_slug = q.get("quest_id", quest_slug)
                        
                        stmt = select(QuestDefinition).where(QuestDefinition.slug == db_quest_slug)
                        existing_quest = (await session.execute(stmt)).scalar_one_or_none()
                        
                        detailed_desc = format_quest_description(q)
                        
                        if not existing_quest:
                            print(f"    - Creating Quest: {db_quest_slug}")
                            quest = QuestDefinition(
                                slug=db_quest_slug,
                                track_id=track_id,
                                world_id=world_slug,
                                title=q["title"],
                                short_description=q["summary"],
                                detailed_description=detailed_desc,
                                rubric_id=db_quest_slug + "_rubric",
                                base_xp_reward=20 * (tier_group.get("tier", 1) * 2), # Scaling XP
                                order_index=index,
                                is_repeatable=True
                            )
                            session.add(quest)
                        else:
                            existing_quest.title = q["title"]
                            existing_quest.short_description = q["summary"]
                            existing_quest.detailed_description = detailed_desc
                            existing_quest.order_index = index
                            session.add(existing_quest)
                            
                    # Upsert Boss if present
                    if "boss" in track_def:
                        b = track_def["boss"]
                        boss_id = b["boss_id"]
                        
                        stmt = select(BossDefinition).where(BossDefinition.id == boss_id)
                        existing_boss = (await session.execute(stmt)).scalar_one_or_none()
                        
                        rubric_text = "**Requirements:**\n" + "\n".join([f"- {r}" for r in b.get("requirements", [])])
                        
                        if not existing_boss:
                            print(f"    - Creating BOSS: {boss_id}")
                            boss = BossDefinition(
                                id=boss_id,
                                name=b["title"],
                                description=b["mission"],
                                rubric=rubric_text, # Storing requirements in logic rubric field for now
                                world_id=world_slug,
                                track_id=track_id,
                                difficulty=b.get("difficulty", "normal")
                            )
                            session.add(boss)
                        else:
                            existing_boss.name = b["title"]
                            existing_boss.description = b["mission"]
                            existing_boss.rubric = rubric_text
                            session.add(existing_boss)
        
        await session.commit()
    print("✅ Expanded Curriculum Seeded.")

if __name__ == "__main__":
    asyncio.run(seed_expanded_curriculum())
