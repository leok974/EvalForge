import json
import os
import re
from pathlib import Path
import sys
from datetime import datetime, date

# --- Configuration Loading ---
SCOPE_PATH = Path("configs/curriculum_guardrail_scope.json")
def load_scope():
    if not SCOPE_PATH.exists():
        return {}
    with open(SCOPE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

SCOPE = load_scope()

def is_active(quest, json_file: Path):
    world_id = quest.get("world_id")
    track_id = quest.get("track_id")
    # Normalize paths
    rel_pack_path = str(json_file.resolve()).replace("\\", "/")
    if "EvalForge/" in rel_pack_path:
        parts = rel_pack_path.split("EvalForge/")
        rel_pack_path = parts[1] if len(parts) > 1 else parts[0]
    
    if world_id in SCOPE.get("active_worlds", []): return True
    if track_id in SCOPE.get("active_tracks", []): return True
    
    active_packs = SCOPE.get("active_questpacks", [])
    if any(rel_pack_path.endswith(p) for p in active_packs): return True
    
    return False

EXCLUSIONS_PATH = Path("configs/quest_exclusions.json")
def load_exclusions():
    if not EXCLUSIONS_PATH.exists(): return {}
    with open(EXCLUSIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Handle both old format (list of strings) and new format (list of objects)
        if "excluded_slugs" in data:
            return {slug: {"slug": slug, "reason": "Legacy", "added_at": "2026-01-01"} for slug in data["excluded_slugs"]}
        if "excluded_quests" in data:
            return {item["slug"]: item for item in data["excluded_quests"]}
    return {}

EXCLUSIONS_MAP = load_exclusions()

def get_exclusion_age(slug):
    exclusion = EXCLUSIONS_MAP.get(slug)
    if not exclusion: return 0
    added_at_str = exclusion.get("added_at", "2026-01-01")
    try:
        added_at = datetime.strptime(added_at_str, "%Y-%m-%d").date()
        today = date(2026, 3, 17) # Reference date from metadata
        return (today - added_at).days
    except:
        return 999 # Treat malformed dates as very old

def get_quest_content(quest, json_file: Path):
    briefing = quest.get("briefing_md", "") or quest.get("description", "")
    tutorial = quest.get("tutorial_md", "")
    
    workspace = quest.get("workspace", {})
    files_from = workspace.get("files_from", "")
    docs_path = None
    if files_from:
        workspace_path = json_file.parent / files_from
        docs_path = workspace_path.parent / "docs"
    
    if not briefing and docs_path and (docs_path / "briefing.md").exists():
        with open(docs_path / "briefing.md", "r", encoding="utf-8") as bf:
            briefing = bf.read()
            
    if not tutorial and docs_path and (docs_path / "tutorial.md").exists():
        with open(docs_path / "tutorial.md", "r", encoding="utf-8") as tf:
            tutorial = tf.read()
            
    return briefing, tutorial, docs_path

def validate_curriculum():
    print("--- EvalForge Curriculum Validator ---")
    
    # 1. Load Valid References for Global Checks
    try:
        with open("data/tracks.json", "r", encoding="utf-8") as f:
            valid_tracks = {t["id"] for t in json.load(f)}
        with open("data/worlds.json", "r", encoding="utf-8") as f:
            valid_worlds = {w["id"] for w in json.load(f)}
    except Exception as e:
        print(f"FATAL: Could not load reference data: {e}")
        sys.exit(2)

    global_errors = []
    active_errors = []
    warnings = []
    slugs = {} # slug -> pack_name

    questpacks_root = Path("data/questpacks")
    # Exclusion criteria: _legacy, golden-tutorials, terms.json
    all_json_files = {f.resolve() for f in questpacks_root.rglob("*.json") 
                      if "_legacy" not in str(f) 
                      and "golden-tutorials" not in str(f)
                      and f.name not in ["terms.json", "config.json"]}
    
    print(f"Inspecting {len(all_json_files)} unique questpack files...")

    for json_file in sorted(all_json_files):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                global_errors.append(f"{json_file.name}: Invalid JSON - {e}")
                continue
            
            quests = []
            pack_world_id = None
            pack_track_id = None
            
            if isinstance(data, list):
                quests = data
            elif isinstance(data, dict):
                # Only treat as questpack if it has 'quests' or 'packs' or starts with quest-like keys
                if "quests" in data or "packs" in data:
                    pack_world_id = data.get("world_id")
                    pack_track_id = data.get("track_id")
                    quests = data.get("quests", data.get("packs", []))
                else:
                    # Skip non-questpack JSONs
                    continue

            for quest in quests:
                slug = quest.get("slug") or quest.get("id")
                if not slug:
                    # Might be a pack definition without slug, skip internal objects
                    continue
                
                # Check Exclusions & Aging
                if slug in EXCLUSIONS_MAP:
                    age = get_exclusion_age(slug)
                    # Check if active for potential failure
                    # We need to compute q_active early here
                    is_q_active = is_active(quest, json_file)
                    
                    if age > 90 and is_q_active:
                        active_errors.append(f"[{json_file.name}] {slug}: Exclusion expired ({age} days old). Please refresh or resolve.")
                    elif age > 30:
                        warnings.append(f"[{json_file.name}] {slug}: Exclusion aging ({age} days old).")
                    
                    continue

                # --- TIER 1: GLOBAL STRUCTURAL CHECKS ---
                if slug in slugs:
                    global_errors.append(f"[{json_file.name}] Duplicate slug '{slug}' (also in {slugs[slug]})")
                slugs[slug] = json_file.name
                
                w_id = quest.get("world_id") or pack_world_id
                if not w_id or w_id not in valid_worlds:
                    global_errors.append(f"[{json_file.name}] {slug}: Invalid/Missing world_id: {w_id}")
                
                t_id = quest.get("track_id") or pack_track_id
                if not t_id or t_id not in valid_tracks:
                    global_errors.append(f"[{json_file.name}] {slug}: Invalid/Missing track_id: {t_id}")

                # --- TIER 2 & 3: QUALITY CHECKS ---
                q_active = is_active(quest, json_file)
                q_issues = []

                # Content Quality
                briefing, tutorial, docs_path = get_quest_content(quest, json_file)
                
                if not quest.get("short_description"):
                    q_issues.append("Missing short_description")
                
                if not briefing or "placeholder" in briefing.lower() or "TODO" in briefing:
                    q_issues.append("Invalid/Placeholder briefing")
                
                if not quest.get("objectives") and not quest.get("objectives_json"):
                    q_issues.append("Missing objectives")
                
                # Workspace / Example Files
                workspace = quest.get("workspace", {})
                files_from = workspace.get("files_from", "")
                if files_from:
                    base_path = json_file.parent / files_from
                    if not base_path.exists():
                        q_issues.append(f"Workspace path does not exist: {files_from}")
                    else:
                        lang = quest.get("language", "python")
                        if lang == "python" and not (base_path / "example.py").exists():
                            q_issues.append("Missing example.py")
                        elif lang == "sql" and not (base_path / "example.sql").exists():
                            q_issues.append("Missing example.sql")

                # Golden Extras
                if q_active:
                    if tutorial and "```" not in tutorial:
                        q_issues.append("Tutorial missing code blocks")
                    if len(quest.get("key_terms", [])) < 3:
                        q_issues.append(f"Insufficient key terms ({len(quest.get('key_terms', []))}/3)")

                # Categorize Issues
                for issue in q_issues:
                    msg = f"[{json_file.name}] {slug}: {issue}"
                    if q_active:
                        active_errors.append(msg)
                    else:
                        warnings.append(msg)

    # --- REPORTING ---
    if warnings:
        print(f"\n🟡 WARNINGS (Non-Active Scope): {len(warnings)}")
            
    if active_errors:
        print(f"\n🔴 FAIL (Active Scope Quality): {len(active_errors)}")
        for e in active_errors[:20]: print(f"  - {e}")
        if len(active_errors) > 20: print(f"  ... and {len(active_errors)-20} more")
        
    if global_errors:
        print(f"\n💀 FAIL (Global Structural): {len(global_errors)}")
        for e in global_errors: print(f"  - {e}")
        
    if global_errors or active_errors:
        print(f"\n❌ Validation Failed: {len(global_errors)} Global, {len(active_errors)} Active Issues.")
        return False
    
    print("\n✅ Validation Passed.")
    return True

if __name__ == "__main__":
    if not validate_curriculum():
        sys.exit(1)
