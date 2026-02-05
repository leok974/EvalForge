import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None

def save_json(path: str, data: Any):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Saved update to {path}")
    except Exception as e:
        print(f"❌ Failed to save {path}: {e}")

def generate_defaults(quest: Dict[str, Any]) -> Dict[str, Any]:
    title = quest.get("title", "Unknown Mission")
    updates = {}
    
    # Briefing
    updates["briefing_md"] = f"""# Mission: {title}

You have been assigned to: **{title}**.

Your objective is to implement the solution according to the specifications.
Check the **Objectives** tab for detailed requirements.
"""

    # Objectives (if missing/empty)
    # If key exists but is empty list, we fill it.
    # If key missing, we add it.
    updates["objectives"] = [
        {"id": "obj_1", "text": "Complete the core implementation", "why": "Demonstrate understanding of the concept"},
        {"id": "obj_2", "text": "Pass all test cases", "why": "Verify correctness"}
    ]
    
    # Lore
    updates["lore_md"] = f"""## System Log: {title}

> *Accessing archival data...*
>
> Subject: {title}
> Status: Active
> Priority: Normal

The system requires your expertise to resolve this challenge.
"""
    return updates

def backfill_file(source_path: str, failures: List[Dict], dry_run: bool):
    # Load source
    full_path = os.path.normpath(os.path.join(os.getcwd(), source_path))
    data = load_json(full_path)
    if not data:
        return

    # Normalize structure (List of quests OR Single Quest Object)
    quests_to_process = []
    is_single_object = False
    
    if isinstance(data, list):
        quests_to_process = data
    elif isinstance(data, dict):
        if "packs" in data: quests_to_process = data["packs"]
        elif "quests" in data: quests_to_process = data["quests"]
        else:
             # It's a single quest object (e.g. docs/quests/x/quest.json)
             quests_to_process = [data]
             is_single_object = True

    modified = False
    
    # Create lookup of failures for this file
    # We match by slug. If single object, we just check if any failure matches.
    failures_map = {f["slug"]: f["missing_fields"] for f in failures if f.get("source_file") == source_path}
    
    # Fallback for old audit format or manual run (match by pack_path if source_file missing)
    if not failures_map:
         failures_map = {f["slug"]: f["missing_fields"] for f in failures if f.get("pack_path") == source_path}

    if not failures_map:
        return

    for q in quests_to_process:
        slug = q.get("slug") or q.get("id")
        
        # Determine if this specific quest needs update
        # If single object, and we have failures mapped to it, proceed.
        if is_single_object and failures_map:
            # For single object, we might match by slug OR just take the first failure if it didn't have a slug (unknown)
            # But with fixed audit script, slug should be known.
            if slug in failures_map:
                missing = failures_map[slug]
            else:
                 # Backup: just use first failure for this file
                 missing = list(failures_map.values())[0]
        elif slug in failures_map:
            missing = failures_map[slug]
        else:
            continue
            
        defaults = generate_defaults(q)
        
        if "briefing_md" in missing:
            if not dry_run: q["briefing_md"] = defaults["briefing_md"]
            modified = True
            
        if "objectives" in missing:
            if not dry_run: q["objectives"] = defaults["objectives"]
            modified = True
            
        if "lore_md" in missing:
            if not dry_run: q["lore_md"] = defaults["lore_md"]
            modified = True
    
    if modified:
        if dry_run:
            print(f"   [DRY-RUN] Would update {source_path}")
        else:
            print(f"   Writing updates to {source_path}...")
            save_json(full_path, data)

def main():
    parser = argparse.ArgumentParser(description="Backfill missing Quest Panels")
    parser.add_argument("--from", dest="source_file", required=True, help="Path to artifacts/quest_panels_audit.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--apply", action="store_true", help="Apply changes to disk")
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.apply:
        print("❌ Must specify either --dry-run or --apply")
        sys.exit(1)
        
    audit_data = load_json(args.source_file)
    if not audit_data:
        sys.exit(1)
        
    # Filter only failed
    failures = [x for x in audit_data if x["status"] == "fail"]
    print(f"🔧 Processing {len(failures)} failed profiles...")
    
    # Group by source_file (prefer 'source_file', fallback to 'pack_path')
    files_to_update = sorted(list(set(x.get("source_file", x.get("pack_path")) for x in failures)))
    
    for fpath in files_to_update:
        if fpath:
            backfill_file(fpath, failures, args.dry_run)
        
    print("\n✅ Backfill processing complete.")

if __name__ == "__main__":
    main()
