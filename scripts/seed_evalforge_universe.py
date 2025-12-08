import asyncio
import json
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

# App Imports
# Adjust these based on your actual structure
from arcade_app.database import engine
from arcade_app.models import (
    TrackDefinition, 
    QuestDefinition, 
    BossDefinition
    # World definition is implicitly just strings in Track/Quest/Boss models currently, 
    # unless you have a WorldDefinition model. Based on models.py seen, there isn't one yet.
    # We will just seed tracks/quests which carry the world_id.
)

BASE_DOCS = Path("d:/EvalForge/docs")

# List of Track Spec Files to Seed
TRACK_SPECS = [
    # PY
    "curriculum_spec.json",  # Original Foundry (might need adaptation if format differs)
    # TS
    "evalforge_prism_track_refraction.json",
    "evalforge_prism_track_spectrum.json",
    # JAVA
    "evalforge_reactor_track_core_circuit.json",
    "evalforge_reactor_track_service_loop.json",
    # REMAINING (SQL, INFRA, AGENTS, GIT, ML)
    "evalforge_world_content_remaining.json",
    "senior_tier_content.json"
]

# List of Boss Definition Files
BOSS_SPECS = [
    "boss_definitions.world-typescript.json",
    "boss_definitions.world-java.json"
    # Python bosses are currently inside curriculum_spec.json or separate?
    # In curriculum_spec.json they are nested.
    # We should support both formats or migrate.
    # For now, we support the new standalone format.
]

def format_quest_description(q):
    """Combine rich fields into a Markdown detailed description."""
    parts = []
    if "narrative_blurb" in q:
         parts.append(f"_{q['narrative_blurb']}_")

    if "objective" in q:
        parts.append(f"**Objective:**\n{q['objective']}")
    
    if "tasks" in q:
        task_list = "\n".join([f"- {t}" for t in q['tasks']])
        parts.append(f"**Tasks:**\n{task_list}")
        
    if "acceptance_criteria" in q:
        # Check if list or dict (some specs might vary)
        ac = q['acceptance_criteria']
        if isinstance(ac, dict):
            # Handle machine/semantic checks format
            if "machine_checks" in ac:
                parts.append("**Machine Checks:**\n" + "\n".join([f"- {c}" for c in ac['machine_checks']]))
            if "semantic_checks" in ac:
                parts.append("**Semantic Checks:**\n" + "\n".join([f"- {c}" for c in ac['semantic_checks']]))
        elif isinstance(ac, list):
            crit_list = "\n".join([f"- {c}" for c in ac])
            parts.append(f"**Acceptance Criteria:**\n{crit_list}")
            
    return "\n\n".join(parts)

async def upsert_track(session, world_slug, track_data):
    track_id = track_data["track_id"]
    print(f"  - 🛤️ Track: {track_id}")
    
    stmt = select(TrackDefinition).where(TrackDefinition.id == track_id)
    existing = (await session.execute(stmt)).scalar_one_or_none()
    
    if not existing:
        track = TrackDefinition(
            id=track_id,
            world_id=world_slug,
            name=track_data["title"],
            description=track_data.get("summary", ""),
            order_index=track_data.get("order_index", 0),
            boss_slug=None # Will calculate if needed
        )
        session.add(track)
    else:
        existing.name = track_data["title"]
        existing.description = track_data.get("summary", "")
        existing.order_index = track_data.get("order_index", 0)
        session.add(existing)

async def upsert_quest(session, world_slug, track_id, quest_data):
    # Allow quest_id to drive the slug if explicit slug is missing
    quest_db_id = quest_data.get("quest_id")
    quest_slug = quest_data.get("slug")
    
    if not quest_slug and quest_db_id:
        quest_slug = quest_db_id  # fallback
        
    if not quest_slug:
        # Should not happen as existing specs usually have one or the other
        print(f"Skipping quest {quest_data.get('title')} (no slug/id)")
        return

    # Use full ID if present, else derived from track + slug
    if not quest_db_id:
        quest_db_id = f"{track_id}-{quest_slug}"
    
    print(f"    - ⚔️ Quest: {quest_db_id}")
    
    stmt = select(QuestDefinition).where(QuestDefinition.slug == quest_db_id)
    existing = (await session.execute(stmt)).scalar_one_or_none()
    
    details = format_quest_description(quest_data)
    
    if not existing:
        quest = QuestDefinition(
            slug=quest_db_id,
            world_id=world_slug,
            track_id=track_id,
            title=quest_data["title"],
            short_description=quest_data.get("summary") or quest_data.get("narrative_blurb", "")[:150],
            detailed_description=details,
            rubric_id=quest_data.get("quest_id") + "_rubric", # default convention
            base_xp_reward=50,
            order_index=quest_data.get("order_index", 0),
            is_repeatable=True
        )
        session.add(quest)
    else:
        existing.title = quest_data["title"]
        existing.short_description = quest_data.get("summary") or quest_data.get("narrative_blurb", "")[:150]
        existing.detailed_description = details
        existing.order_index = quest_data.get("order_index", 0)
        session.add(existing)

async def upsert_boss(session, boss_data):
    boss_id = boss_data["boss_id"]
    print(f"  - 👹 Boss: {boss_id}")
    
    stmt = select(BossDefinition).where(BossDefinition.id == boss_id)
    existing = (await session.execute(stmt)).scalar_one_or_none()
    
    if not existing:
        boss = BossDefinition(
            id=boss_id,
            name=boss_data["title"],
            description=boss_data.get("long_description", "") or boss_data.get("mission", ""),
            world_id=boss_data.get("world_slug"),
            track_id=boss_data.get("track_id"),
            difficulty=boss_data.get("difficulty", "normal"),
            rubric=boss_data.get("rubric_id") or boss_data.get("rubric") or boss_id,
            # If model expects raw text rubric, we might need to fetch it. 
            # But recent patterns seem to use rubric_id pointer for JSON rubrics.
            # We'll store the ID here if it looks like an ID, helpful for frontend lookup.
            hint_codex_id=boss_data.get("hint_codex_id")
        )
        session.add(boss)
    else:
        existing.name = boss_data["title"]
        existing.description = boss_data.get("long_description", "") or boss_data.get("mission", "")
        existing.hint_codex_id = boss_data.get("hint_codex_id")
        existing.rubric = boss_data.get("rubric_id") or boss_data.get("rubric") or boss_id
        session.add(existing)

async def seed_universe():
    print("🌌 Seeding EvalForge Universe...")
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        
        # 1. Seed Tracks & Quests from JSON Specs
        for spec_file in TRACK_SPECS:
            path = BASE_DOCS / spec_file
            if not path.exists():
                print(f"⚠️ Spec not found: {spec_file}")
                # Try fallback location if it's the old curriculum
                if spec_file == "curriculum_spec.json":
                     path = Path("d:/EvalForge/arcade_app/curriculum_spec.json")
                
                if not path.exists():
                     continue

            print(f"📝 Loading Spec: {spec_file}")
            data = json.loads(path.read_text(encoding="utf-8"))
            
            # Handle list vs dict (Old spec is list of worlds, New spec is single object Snapshot)
            if isinstance(data, list):
                # Old Format (The Foundry)
                for world in data:
                    world_slug = world["world_slug"]
                    for tier in world.get("tier_tracks", []):
                        for track in tier["tracks"]:
                            await upsert_track(session, world_slug, track)
                            for q in track["tracks"] if "tracks" in track else track["quests"]: # confusion in old key naming?
                                # old spec: tracks -> list of track inputs. track input has "quests" list.
                                await upsert_quest(session, world_slug, track["track_id"], q)
                                
                            if "boss" in track:
                                # Old embedded boss format -> convert to flat boss def?
                                # For parity, we can upsert checks here too.
                                b = track["boss"]
                                b_data = {
                                    "boss_id": b["boss_id"],
                                    "title": b["title"],
                                    "long_description": b["mission"],
                                    "world_slug": world_slug,
                                    "track_id": track["track_id"],
                                    "difficulty": b.get("difficulty"),
                                    "rubric_id": f"rubric-{b['boss_id']}" # convention
                                }
                                await upsert_boss(session, b_data)

            elif isinstance(data, dict) and data.get("snapshot_kind") == "evalforge_track_spec":
                # New Format (The Prism)
                world_slug = data["world_slug"]
                track_data = data["track"]
                await upsert_track(session, world_slug, track_data)
                
                for q in data["quests"]:
                    await upsert_quest(session, world_slug, track_data["track_id"], q)
                    
                # Boss Stubs in Track Spec?
                if "boss_stub" in data:
                    # Just a stub, full def is in BOSS_SPECS usually.
                    print(f"    (Found boss stub {data['boss_stub']['boss_id']}, expecting full def in boss list)")

            elif isinstance(data, dict) and data.get("snapshot_kind") == "evalforge_world_content":
                # New Format (Remaining Worlds Snapshot)
                for world in data["worlds"]:
                    world_slug = world["world_slug"]
                    print(f"🌍 Seeding World: {world_slug}")
                    
                    for track in world.get("tracks", []):
                        await upsert_track(session, world_slug, track)
                        
                        for q in track.get("quests", []):
                            await upsert_quest(session, world_slug, track["track_id"], q)
                            
                        for boss in track.get("bosses", []):
                             # Need to make sure title -> name mapping is handled or assumes corrected key
                             # We fixed json to use 'title', so upsert_boss works if we pass it correctly
                             await upsert_boss(session, boss)
                    
                    for boss in world.get("bosses", []):
                        # Use upsert_boss, assuming structure matches
                        # The snapshot has slightly different keys (e.g. 'title' instead of 'name')
                        # upsert_boss expects 'title' in input data based on existing code:
                        # boss_data["title"] -> name
                        await upsert_boss(session, boss)
            
        # 2. Seed Boss Definitions from Standalone Files
        for boss_spec in BOSS_SPECS:
            path = BASE_DOCS / boss_spec
            if not path.exists():
                print(f"⚠️ Boss Spec not found: {boss_spec}"); continue
                
            print(f"👹 Loading Boss Spec: {boss_spec}")
            data = json.loads(path.read_text(encoding="utf-8"))
            
            for b_data in data["bosses"]:
                await upsert_boss(session, b_data)

        await session.commit()
        print("✅ Universe Seeded Successfully.")

if __name__ == "__main__":
    # Ensure env allows import
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(seed_universe())
