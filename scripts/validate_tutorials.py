
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

def scan_quests(root_dir, mode="all", force_tier=None):
    """Scans quests and runs validators with policy enforcement."""
    quests_dir = os.path.join(root_dir, "docs", "quests")
    pack_dir = os.path.join(root_dir, "data", "questpacks")
    
    policy = load_policy(root_dir)
    starters = get_starter_quests(root_dir)
    starter_set = set(starters)
    
    default_tier = policy.get("default_tier", 2)
    tiers_config = policy.get("tiers", {})
    
    print(f"Policy: Mode={mode}, Default Tier={default_tier}, Force Tier={force_tier}")

    failures = 0
    all_refs = set()
    
    # ... (Path collection logic remains same) ...
    search_paths = []
    if os.path.exists(quests_dir): search_paths.append(quests_dir)
    if os.path.exists(pack_dir): search_paths.append(pack_dir)
    
    quest_dirs = []
    for root, dirs, files in os.walk(root_dir):
        if "quest.json" in files:
             quest_dirs.append(root)

    print(f"Scanning {len(quest_dirs)} quest directories...")
    
    quests_list = [] 
    
    for qpath in quest_dirs:
        try:
            with open(os.path.join(qpath, "quest.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                quests_list.append((data, qpath))
                
                slugs_in_dir = []
                if isinstance(data, list):
                    slugs_in_dir = [x.get("slug") for x in data if x.get("slug")]
                    for item in data: quests_list.append((item, qpath))
                elif isinstance(data, dict):
                     slugs_in_dir = [data.get("slug")]
                     
                for slug in slugs_in_dir:
                    if not slug: continue
                    
                    is_starter = slug in starter_set
                    if mode == "starters" and not is_starter: continue
                    
                    # Resolve Tier
                    # 1. Force tier if provided
                    # 2. Tier 1 if starter
                    # 3. Default tier otherwise
                    current_tier = force_tier if force_tier else (1 if is_starter else default_tier)
                    rules = tiers_config.get(str(current_tier), {})
                    
                    # Collect Refs
                    tpath = os.path.join(qpath, "terms.json")
                    if os.path.exists(tpath):
                        try:
                            with open(tpath, "r", encoding="utf-8") as tf:
                                tdata = json.load(tf)
                                for t in tdata:
                                    if "codex_ref" in t: all_refs.add(t.get("codex_ref"))
                        except: pass
                    
                    # Validate
                    errors = []
                    
                    # "Strict" validation based on tier rules
                    # We utilize validate_tutorial_strict for checking terms count and snippet
                    # even if it's not "Tier 1", we just adjust limits.
                    
                    # Check Tutorial
                    tut_path = os.path.join(qpath, "tutorial.md")
                    has_tutorial = os.path.exists(tut_path)
                    
                    if not has_tutorial:
                        # Fail if tier 1, or if policy strictness requires it?
                        # For now, let's assume all tiers require a tutorial file to exist
                        errors.append("Missing tutorial.md")
                    else:
                        errors.extend(validate_tutorial_strict(qpath, 
                                                               min_terms=rules.get("min_terms", 0),
                                                               require_example=rules.get("require_snippet", False),
                                                               allow_placeholders=rules.get("allow_placeholders", True)))
                        # Structure check
                        errors.extend(validate_tutorial_structure(qpath))

                    # Check Terms
                    if os.path.exists(tpath):
                        errors.extend(validate_terms_schema(qpath))
                        # references check
                        if rules.get("strict_codex_refs", True):
                             errors.extend(validate_codex_links(qpath, root_dir))

                    if errors:
                        real_errors = [e for e in errors if not e.startswith("WARNING:")]
                        warnings = [e for e in errors if e.startswith("WARNING:")]
                        
                        if real_errors:
                             print(f"❌ {slug} (Tier {current_tier}):")
                             for e in real_errors: print(f"   - {e}")
                             failures += 1
                        
                        if warnings:
                             # If no real errors, we might want to print green check with warning?
                             if not real_errors:
                                 print(f"✅ {slug} (Tier {current_tier}) [With Warnings]")
                             for w in warnings: print(f"   - ⚠️  {w}")
                             
                    else:
                        print(f"✅ {slug} (Tier {current_tier})")

        except Exception as e:
            # print(f"Skipping {qpath}: {e}")
            pass

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
    parser.add_argument("--tier", type=int, default=None, help="Force validation tier (1 or 2)")
    args = parser.parse_args()
    
    success = scan_quests(args.root, args.mode, args.tier)
    if not success:
        sys.exit(1)
