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

BASE_DOCS = Path(__file__).parent.parent / "docs"

# List of Track Spec Files to Seed
TRACK_SPECS = [
    # PY
    # "curriculum_spec.json",  <-- Legacy
    "../data/questpacks/_modern/python_foundry_core.json",
    # TS
    "evalforge_prism_track_refraction.json",
    "evalforge_prism_track_spectrum.json",
    # JAVA
    "evalforge_reactor_track_core_circuit.json",
    "evalforge_reactor_track_service_loop.json",
    # REMAINING (SQL, INFRA, AGENTS, GIT, ML)
    "evalforge_world_content_remaining.json",
    "senior_tier_content.json",
    "../data/questpacks/_tier2/python_tier2.json",
    "../data/questpacks/_tier2/sql_tier2.json",
    "../data/questpacks/_tier2/git_tier2.json",
    "../data/questpacks/sql_tier3/sql_tier3.json"
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

async def upsert_quest(session, world_slug, track_id, quest_data, seeded_slugs=None):
    # Allow quest_id to drive the slug if explicit slug is missing
    quest_db_id = quest_data.get("quest_id")
    quest_slug = quest_data.get("slug")
    
    if not quest_slug and quest_db_id:
        quest_slug = quest_db_id  # fallback
        
def build_quest_workspace(quest_dir: Path, quest_data: dict) -> dict:
    """Extracts and builds the workspace payload consistently including nested fixtures."""
    import copy
    workspace_json = copy.deepcopy(quest_data.get("workspace") or {"files": []})
    workspace_json["files"] = []
    
    workspace_dir = quest_dir / "workspace"
    if workspace_dir.exists():
        for p in workspace_dir.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(workspace_dir).as_posix()
            workspace_json["files"].append({
                "path": rel,
                "content": p.read_text(encoding="utf-8"),
                "editable": True
            })
        
    # Preserve metadata fields
    for key in ["db_engine", "featured_tables", "db_explorer_mode"]:
        if key in quest_data:
            workspace_json[key] = quest_data[key]
            
    return workspace_json

async def upsert_quest(session, quest_data, world_slug, track_id, seeded_slugs=None):
    quest_slug = quest_data.get("slug")
    if not quest_slug:
        quest_slug = quest_data.get("quest_id")
        
    if not quest_slug:
        # Should not happen as existing specs usually have one or the other
        print(f"Skipping quest {quest_data.get('title')} (no slug/id)")
        return

    quest_db_id = quest_data.get("id") or quest_data.get("quest_id")
    # Use full ID if present, else derived from track + slug
    if not quest_db_id:
        quest_db_id = f"{track_id}-{quest_slug}"
    
    print(f"    - ⚔️ Quest: {quest_db_id}")
    if seeded_slugs is not None:
        seeded_slugs.add(quest_db_id)
    
    stmt = select(QuestDefinition).where(QuestDefinition.slug == quest_db_id)
    existing = (await session.execute(stmt)).scalar_one_or_none()
    
    details = format_quest_description(quest_data)
    
    # Smart quest_dir discovery
    quest_dir = None
    scp = quest_data.get("starting_code_path")
    if scp:
        # e.g. data/questpacks/sql_tier3/postgres-schema-explorer/workspace/task.sql
        # quest_dir should be up 2 levels from the file in 'workspace'
        p = (BASE_DOCS / ".." / scp).parent
        if p.name == "workspace":
            quest_dir = p.parent
            
    if not quest_dir or not quest_dir.exists():
        # Fallback 1: data/quests/
        quest_dir = BASE_DOCS / ".." / "data" / "quests" / quest_slug
        
    if not quest_dir.exists():
        # Fallback 2: Check for quest.json in tier packs
        # (This is more complex, but scp check usually wins for evalforge)
        pass
        
    workspace_json = build_quest_workspace(quest_dir, quest_data)
    
    if not existing:
        quest = QuestDefinition(
            slug=quest_db_id,
            world_id=world_slug,
            track_id=track_id,
            title=quest_data["title"],
            short_description=quest_data.get("summary") or quest_data.get("narrative_blurb", "")[:150],
            detailed_description=details,
            rubric_id=quest_db_id + "_rubric", # default convention
            base_xp_reward=50,
            order_index=quest_data.get("order_index", 0),
            is_repeatable=True,
            tiered_hints_json=quest_data.get("tiered_hints"),
            key_terms=quest_data.get("key_terms"),
            objectives_json=quest_data.get("objectives"),
            workspace_json=workspace_json,
            grading_json=quest_data.get("grading_json"),
            language=quest_data.get("language"),
            starter_code=quest_data.get("starter_code"),
            briefing_md=quest_data.get("briefing_md") or details or quest_data.get("description", "No briefing provided."),
            tutorial_md=quest_data.get("tutorial_md"),
            lore_md=quest_data.get("lore_md")
        )
        session.add(quest)
    else:
        existing.title = quest_data["title"]
        existing.short_description = quest_data.get("summary") or quest_data.get("narrative_blurb", "")[:150]
        existing.detailed_description = details
        existing.order_index = quest_data.get("order_index", 0)
        existing.tiered_hints_json = quest_data.get("tiered_hints")
        existing.key_terms = quest_data.get("key_terms")
        existing.objectives_json = quest_data.get("objectives")
        existing.workspace_json = workspace_json
        existing.grading_json = quest_data.get("grading_json")
        existing.starter_code = quest_data.get("starter_code")
        existing.briefing_md = quest_data.get("briefing_md") or details or quest_data.get("description", "No briefing provided.")
        existing.tutorial_md = quest_data.get("tutorial_md")
        existing.lore_md = quest_data.get("lore_md")
        if "language" in quest_data:
            existing.language = quest_data["language"]
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
    seeded_slugs = set()
    
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
                                await upsert_quest(session, world_slug, track["track_id"], q, seeded_slugs=seeded_slugs)
                                
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
                    await upsert_quest(session, q, world_slug, track_data["track_id"], seeded_slugs=seeded_slugs)
                    
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
                            await upsert_quest(session, q, world_slug, track["track_id"], seeded_slugs=seeded_slugs)
                            
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
                        
            elif isinstance(data, dict) and "quests" in data and "snapshot_kind" not in data:
                # Flat format (e.g. Tier 2 Packs)
                for q in data["quests"]:
                    # These flat quests must self-describe their world id and track id via json schema
                    await upsert_quest(session, q, q.get("world_id", "world-sql"), q.get("track_id", "core-sql"), seeded_slugs=seeded_slugs)
            
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
        return seeded_slugs

if __name__ == "__main__":
    # Ensure env allows import
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(seed_universe())
