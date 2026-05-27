from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Dict, List, Any, Optional
import logging

from arcade_app.database import get_session
from arcade_app.auth_helper import get_current_user
from arcade_app.models import QuestDefinition, TrackDefinition
from arcade_app.services.quest_visibility import get_active_quest_config
from arcade_app.worlds_helper import load_worlds

router = APIRouter(prefix="/api/workshop", tags=["workshop"])
logger = logging.getLogger(__name__)

@router.get("/catalog")
async def get_workshop_catalog(
    session: Session = Depends(get_session),
    user_data: Dict = Depends(get_current_user)
):
    """
    Returns the active-only catalog of Worlds and Tracks.
    Used to populate the Workshop header and filters dynamically.
    """
    if not user_data:
         # Workshop usually requires auth, but if public catalog is needed allow it?
         # Most API endpoints enforce auth. Let's enforce it.
         raise HTTPException(status_code=401, detail="Not authenticated")

    # 1. Get active slugs from config (The source of truth for "Active")
    active_slugs, _ = get_active_quest_config()

    if not active_slugs:
        return {
            "worlds": [],
            "tracks": [],
            "defaults": {"name_mode_default": "lore"}
        }

    # 2. Fetch Active Quests to discover active Worlds/Tracks
    # We only care about quests that are in the active whitelist.
    statement = select(QuestDefinition).where(QuestDefinition.slug.in_(active_slugs))
    results = await session.exec(statement)
    active_quests = results.all()

    # 3. Load World Metadata (for Lore Names/Icons)
    # This comes from data/worlds.json
    worlds_meta = load_worlds()  # Dict[world_id, WorldDict]

    # --- DEFINITIONS & ALIASES ---
    # Sprint 23: Standardised to <world>-<tier> convention.
    # Migration map (old ID -> new canonical ID):
    #   python-fundamentals        -> python-foundry
    #   foundry-senior-systems     -> python-systems
    #   fundamentals               -> python-foundry
    #   boss-prep                  -> python-boss
    #   core-python                -> python-ignition
    #   js-ignition/arrays/etc.    -> js-foundry
    #   ts-fundamentals            -> ts-foundry
    #   git-fundamentals           -> git-foundry
    #   track-sql                  -> sql-foundry
    #   track-html                 -> web-html  (content-based, not tier)
    #   track-css                  -> web-css   (content-based, not tier)
    #   track-docker-ignition      -> docker-ignition
    #   track-docker-systems       -> docker-systems
    TRACK_ALIASES = {
        # Legacy python aliases
        "fundamentals": "python-foundry",
        "python-fundamentals": "python-foundry",
        "foundry-senior-systems": "python-systems",
        "core-python": "python-ignition",
        "boss-prep": "python-boss",
        # Legacy JS module tracks (consolidated to one foundry track)
        "js-ignition": "js-foundry",
        "js-arrays": "js-foundry",
        "js-objects": "js-foundry",
        "js-functions": "js-foundry",
        "js-async": "js-foundry",
        "js-errors": "js-foundry",
        "js-modules": "js-foundry",
        # Legacy TS / Git
        "ts-fundamentals": "ts-foundry",
        "git-fundamentals": "git-foundry",
        "core-git": "git-systems",
        # Legacy web / sql / docker
        "track-sql": "sql-foundry",
        "track-html": "web-html",
        "track-css": "web-css",
        "track-docker-ignition": "docker-ignition",
        "track-docker-systems": "docker-systems",
        # Old curriculum-scope prefix style
        "track-python-foundry": "python-foundry",
        "track-python-ignition": "python-ignition",
        "track-python-systems": "python-systems",
        "track-python-selenium": "python-selenium",
    }

    # Hardcoded display names for tracks missing from the DB TrackDefinition table.
    # Keys are canonical IDs. Legacy aliases are resolved via TRACK_ALIASES above.
    HARDCODED_TRACKS = {
        # Canonical Python tracks
        "python-foundry":   {"name": "Python Foundry",   "order_index": 1},
        "python-ignition":  {"name": "Python Ignition",  "order_index": 2},
        "python-systems":   {"name": "Python Systems",   "order_index": 3},
        "python-boss":      {"name": "Python Boss",      "order_index": 4},
        "python-selenium":  {"name": "Python Selenium",  "order_index": 5},
        # Canonical JS / TS / Git tracks
        "js-foundry":       {"name": "JS Foundry",       "order_index": 1},
        "ts-foundry":       {"name": "TS Foundry",       "order_index": 1},
        "git-foundry":      {"name": "Git Foundry",      "order_index": 1},
        "git-systems":      {"name": "Git Systems",      "order_index": 2},
        # Canonical SQL / Web / Docker tracks
        "sql-foundry":      {"name": "SQL Foundry",      "order_index": 1},
        "web-html":         {"name": "HTML",              "order_index": 1},
        "web-css":          {"name": "CSS",               "order_index": 2},
        "docker-ignition":  {"name": "Docker Ignition",  "order_index": 1},
        "docker-systems":   {"name": "Docker Systems",   "order_index": 2},
        # Misc
        "misc":             {"name": "Miscellaneous",    "order_index": 999},
        "core":             {"name": "Core Concepts",    "order_index": 5},
        # CLI / Node / React (inactive but keep for catalog completeness)
        "track-cli-core":        {"name": "CLI Core",          "order_index": 2},
        "cli-fundamentals":      {"name": "CLI Fundamentals",  "order_index": 1},
        "track-node-core":       {"name": "Node Core",         "order_index": 2},
        "node-fundamentals":     {"name": "Node Fundamentals", "order_index": 1},
        "track-react":           {"name": "React Core",        "order_index": 2},
        "react-fundamentals":    {"name": "React Fundamentals","order_index": 1},
    }

    # 4. Aggregate Tracks and Worlds present in Active Quests
    active_world_ids = set()
    active_track_ids = set()
    
    world_quest_counts = {}
    track_quest_counts = {} # Key: (world_id, track_id) -> count

    discovered_pairs = set() # Set of (world_id, track_id)

    for q in active_quests:
        w_id = q.world_id
        t_id = q.track_id
        
        # Apply Alias to Track ID (Normalization)
        if t_id in TRACK_ALIASES:
            t_id = TRACK_ALIASES[t_id]
        
        if w_id:
            active_world_ids.add(w_id)
            world_quest_counts[w_id] = world_quest_counts.get(w_id, 0) + 1
        
        if t_id and w_id:
            active_track_ids.add(t_id)
            
            pair = (w_id, t_id)
            discovered_pairs.add(pair)
            track_quest_counts[pair] = track_quest_counts.get(pair, 0) + 1

    # 5. Fetch definitions for discovered Tracks to get proper display names
    # (If track is not in DB but referenced in quest, we fallback to ID)
    track_defs_map = {}
    if active_track_ids:
        track_stmt = select(TrackDefinition).where(TrackDefinition.id.in_(active_track_ids))
        track_results = await session.exec(track_stmt)
        for t in track_results.all():
            track_defs_map[t.id] = t

    # 6. Build Response Objects

    # --- WORLDS ---
    catalog_worlds = []
    # Iterate over metadata order to preserve explicit ordering if defined there
    # (JSON lists preserve order).
    
    for w_id, w_data in worlds_meta.items():
        if w_id in active_world_ids:
            # Determine Lore Name
            # "alias" in narrative_config is usually the Lore/Fancy name (e.g. "The Foundry")
            # "name" is often "Python World".
            # "id" is "world-python".
            
            narrative = w_data.get("narrative_config", {})
            alias = narrative.get("alias")
            
            # Logic:
            # Lore Name = Alias ("The Foundry") or Name ("Python World")
            # Real Name = ID ("world-python")
            
            lore_name = alias if alias else w_data.get("name", w_id)
            
            catalog_worlds.append({
                "world_id": w_id,
                "real_name": w_id,
                "lore_name": lore_name.title() if lore_name else w_id, 
                "display_name": w_data.get("name", w_id),
                "icon": w_data.get("icon", "box"),
                "quest_count": world_quest_counts.get(w_id, 0),
                "order": 0 # TODO: Could derive from worlds.json list index
            })
            
    # Include worlds that might have been missed if worlds.json is incomplete but DB has quests?
    # Usually worlds.json is authoritative for UI. If missing from there, UI might break.
    # We skip them or add defaults. Let's stick to strict intersection for safety.

    # --- TRACKS ---
    catalog_tracks = []
    
    # Iterate over discovered pairs to allow same track_id in multiple worlds
    for w_id, t_id in discovered_pairs:
        t_def = track_defs_map.get(t_id)
        
        # Resolutions: DB > Hardcoded > Raw ID
        
        # Real Name = ID
        real_name = t_id
        
        # Lore Name
        lore_name = t_id 
        if t_def:
            lore_name = t_def.name
        elif t_id in HARDCODED_TRACKS:
            lore_name = HARDCODED_TRACKS[t_id]["name"]
            
        # Order
        order_index = 999
        if t_def:
            order_index = t_def.order_index
        elif t_id in HARDCODED_TRACKS:
            order_index = HARDCODED_TRACKS[t_id]["order_index"]
        
        catalog_tracks.append({
            "track_id": t_id,
            "world_id": w_id,
            "real_name": real_name,
            "lore_name": lore_name,
            "quest_count": track_quest_counts.get((w_id, t_id), 0),
            "order_index": order_index
        })
        
    # Sort tracks
    catalog_tracks.sort(key=lambda x: (x["world_id"], x["order_index"]))

    return {
        "worlds": catalog_worlds,
        "tracks": catalog_tracks,
        "aliases": TRACK_ALIASES,
        "defaults": {
            "name_mode_default": "lore"
        }
    }
