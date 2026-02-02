
import os
import sys
import argparse
import json
# Local import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.validators import validate_tutorial_structure, validate_terms_schema, validate_codex_links, validate_tutorial_strict, find_codex_orphans
from utils.universe import get_starter_quests

def load_policy(root_dir):
    try:
        with open(os.path.join(root_dir, "configs", "tutorial_policy.json"), "r") as f:
            return json.load(f)
    except:
        return {}

def scan_quests(root_dir, mode="all"):
    """Scans quests and runs validators with policy enforcement."""
    quests_dir = os.path.join(root_dir, "docs", "quests")
    pack_dir = os.path.join(root_dir, "data", "questpacks")
    
    policy = load_policy(root_dir)
    starters = get_starter_quests(root_dir)
    starter_set = set(starters)
    
    print(f"Policy: Mode={mode}, Strict Starters={policy.get('strict_starters')}")
    if mode == "starters":
        print(f"Focusing on {len(starters)} starter quests.")

    failures = 0
    all_refs = set()
    
    # We need to find ALL quests (docs + packs)
    # Reusing find logic or just walking?
    # For validation, we need the directory on disk.
    
    search_paths = []
    if os.path.exists(quests_dir): search_paths.append(quests_dir)
    if os.path.exists(pack_dir): search_paths.append(pack_dir)
    
    quest_dirs = []
    
    # 1. Collect all quest directories
    for root, dirs, files in os.walk(root_dir):
        if "quest.json" in files:
             # Basic check if it's a quest dir
             quest_dirs.append(root)

    print(f"Scanning {len(quest_dirs)} quest directories...")
    
    quests_list = [] # Store tuple (data, path)
    
    for qpath in quest_dirs:
        try:
            with open(os.path.join(qpath, "quest.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                quests_list.append((data, qpath))
                
                # Handle list-based packs (skip, or iterate if we can map back to dir?)
                # If quest.json is a list, this directory is a pack root, ensuring we validating individual items?
                # Actually, our structure is:
                # - docs/quests/{slug}/quest.json (Dict)
                # - data/questpacks/.../quest.json (List of Dicts OR Dict)
                # If it is a list, we might have multiple quests sharing this directory (assets).
                
                slugs_in_dir = []
                if isinstance(data, list):
                    slugs_in_dir = [x.get("slug") for x in data if x.get("slug")]
                    # For missing check, we need to flatten
                    for item in data: quests_list.append((item, qpath))
                elif isinstance(data, dict):
                     slugs_in_dir = [data.get("slug")]
                     
                for slug in slugs_in_dir:
                    if not slug: continue
                    
                    is_starter = slug in starter_set
                    
                    # Filtering based on mode
                    if mode == "starters" and not is_starter: continue
                    
                    # Collect Refs for Orphan check
                    # Collect Refs for Orphan check
                    tpath = os.path.join(qpath, "terms.json")
                    if os.path.exists(tpath):
                        try:
                            with open(tpath, "r", encoding="utf-8") as tf:
                                tdata = json.load(tf)
                                for t in tdata:
                                    if "codex_ref" in t: 
                                        all_refs.add(t.get("codex_ref"))
                                        # if "infra/shell" in t.get("codex_ref"):
                                        #     print(f"DEBUG: Found infra/shell ref in {slug}")
                        except Exception as e:
                            print(f"DEBUG: Error loading terms {tpath}: {e}")
                            pass
                    
                    # Validate
                    errors = []
                    
                    if is_starter and policy.get("strict_starters"):
                         errors = validate_tutorial_strict(qpath, 
                                                           min_terms=policy.get("strict_starters_min_terms", 2),
                                                           require_example=policy.get("strict_starters_require_example", True))
                         # Add normal link validation too
                         errors.extend(validate_codex_links(qpath, root_dir))
                    else:
                        # Non-starter (or lax mode)
                        # Check existance only if present
                        if os.path.exists(os.path.join(qpath, "tutorial.md")):
                            errors.extend(validate_tutorial_structure(qpath))
                        if os.path.exists(os.path.join(qpath, "terms.json")):
                            errors.extend(validate_terms_schema(qpath))
                            errors.extend(validate_codex_links(qpath, root_dir))

                    if errors:
                        print(f"❌ {slug}:")
                        for e in errors: print(f"   - {e}")
                        failures += 1
                    elif mode == "starters" or (mode == "all" and is_starter):
                        print(f"✅ {slug}")

        except Exception as e:
            # print(f"Skipping {qpath}: {e}")
            pass

    # Orphan Check
    orphans = find_codex_orphans(root_dir, all_refs)
    if orphans:
        print(f"\n⚠️  Found {len(orphans)} Orphaned Codex Pages:")
        if policy.get("codex_orphan_mode") == "strict":
             print("   (Strict mode enabled - Failing)")
             failures += 1
        else:
             print("   (Warn only)")
             
        for o in orphans[:10]:
            print(f"   - {o}")
        if len(orphans) > 10: print(f"   ... and {len(orphans)-10} more")
        
        # Write report
        with open("codex_orphans.json", "w") as f:
            json.dump(orphans, f, indent=2)

    # Missing Starters Check (Phase 9.3)
    if mode == "starters":
        seen_starters = set()
        for q, _ in quests_list:
             s = q.get("slug")
             if s in starter_set:
                 seen_starters.add(s)
                 
        missing = starter_set - seen_starters
        if missing:
             print(f"\n❌ Missing {len(missing)} Starter Quests (Must exist on disk):")
             for m in missing:
                 print(f"   - {m}")
             failures += 1
    
    return failures == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--mode", choices=["all", "starters", "changed"], default="all")
    args = parser.parse_args()
    
    success = scan_quests(args.root, args.mode)
    if not success:
        sys.exit(1)
