import os
import json
import glob
import sys
from pathlib import Path

# Reuse scope logic from curriculum_validator style
SCOPE_PATH = Path("configs/curriculum_guardrail_scope.json")
def load_scope():
    if not SCOPE_PATH.exists():
        return {}
    with open(SCOPE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

SCOPE = load_scope()

def is_active(quest, pack_name):
    world_id = quest.get("world_id")
    track_id = quest.get("track_id")
    if world_id in SCOPE.get("active_worlds", []): return True
    if track_id in SCOPE.get("active_tracks", []): return True
    active_packs = SCOPE.get("active_questpacks", [])
    if any(pack_name.endswith(p) for p in active_packs): return True
    return False

def audit_quests():
    questpacks_path = os.path.join("data", "questpacks", "**", "*.json")
    files = glob.glob(questpacks_path, recursive=True)
    
    global_errors = []
    active_errors = []
    warnings = []
    
    total_quests = 0
    slugs = set()
    
    # 1. Load Valid References
    try:
        with open(os.path.join("data", "tracks.json"), "r", encoding="utf-8") as f:
            valid_tracks = {t["id"] for t in json.load(f)}
        with open(os.path.join("data", "worlds.json"), "r", encoding="utf-8") as f:
            valid_worlds = {w["id"] for w in json.load(f)}
    except Exception as e:
        print(f"FATAL: Could not load reference data: {e}")
        sys.exit(2)

    for f_path in files:
        pack_name = os.path.basename(f_path)
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            global_errors.append(f"JSON_PARSE_ERROR in {pack_name}: {e}")
            continue
            
        quests = []
        pack_world_id = None
        pack_track_id = None
        
        if isinstance(data, list):
            quests = data
        elif isinstance(data, dict):
            pack_world_id = data.get("world_id")
            pack_track_id = data.get("track_id")
            quests = data.get("quests", data.get("packs", []))
        
        for q in quests:
            total_quests += 1
            slug = q.get("slug") or q.get("id")
            if not slug:
                global_errors.append(f"[{pack_name}] Quest is missing both 'slug' and 'id'")
                continue

            q_active = is_active(q, pack_name)
            q_issues = []

            # --- GLOBAL CHECKS ---
            if slug in slugs:
                global_errors.append(f"[{pack_name}] Duplicate slug found: '{slug}'")
            slugs.add(slug)

            t_id = q.get("track_id") or pack_track_id
            if not t_id or t_id not in valid_tracks:
                global_errors.append(f"[{pack_name}] Quest '{slug}' has invalid track_id: {t_id}")
            
            w_id = q.get("world_id") or pack_world_id
            if not w_id or w_id not in valid_worlds:
                global_errors.append(f"[{pack_name}] Quest '{slug}' has invalid world_id: {w_id}")

            # --- QUALITY CHECKS (Active vs Warn) ---
            if not q.get("short_description"):
                q_issues.append("missing short_description")
            
            if q.get("requires_app_preview") and not q.get("app_entry_path"):
                q_issues.append("requires_app_preview but missing app_entry_path")

            has_starter = q.get("starter_code") or (q.get("workspace_json") and q["workspace_json"].get("files")) or q.get("workspace")
            if not has_starter:
                q_issues.append("missing starter_code or workspace")

            for issue in q_issues:
                msg = f"[{pack_name}] {slug}: {issue}"
                if q_active:
                    active_errors.append(msg)
                else:
                    warnings.append(msg)

    print(f"Audit complete. Inspected {total_quests} quests in {len(files)} packs.")
    
    if warnings:
        print("\n🟡 WARNINGS (Non-Active Scope):")
        for w in warnings: print(f"  - {w}")
            
    if active_errors:
        print("\n🔴 FAIL (Active Scope):")
        for e in active_errors: print(f"  - {e}")
        
    if global_errors:
        print("\n💀 FAIL (Global Structural):")
        for e in global_errors: print(f"  - {e}")
        
    if global_errors or active_errors:
        print(f"\n❌ Audit Failed: {len(global_errors)} Global, {len(active_errors)} Active Issues.")
        sys.exit(1)
    else:
        print("\n✅ All active quests passed canonical metadata validation.")
        sys.exit(0)

if __name__ == "__main__":
    audit_quests()
