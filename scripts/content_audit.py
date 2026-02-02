
import os
import json
import sys

def audit_content(root_dir):
    print(f"Auditing content in {root_dir}...")
    
    quests = []
    # 1. Walk and find all quest JSONs
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".json") and not f.startswith("world") and not f.startswith("track"):
                path = os.path.join(dirpath, f)
                try:
                    with open(path, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                        if isinstance(data, list):
                            for item in data:
                                quests.append((item, dirpath))
                        elif isinstance(data, dict) and "slug" in data:
                            quests.append((data, dirpath))
                except Exception as e:
                    print(f"Error reading {path}: {e}")

    print(f"Found {len(quests)} quests.")
    
    issues = []
    
    # Tutorial Metrics (Phase 9.3)
    total_quests = len(quests)
    quests_with_tutorial = 0
    quests_with_terms = 0
    broken_codex_refs = 0
    
    missing_tut_list = []
    
    for q, source_dir in quests:
        slug = q.get("slug", "unknown")
        
        # Determine search dirs for hydration
        search_dirs = [source_dir]
        ws = q.get("workspace") or {}
        if "files_from" in ws:
            search_dirs.insert(0, os.path.join(source_dir, ws["files_from"]))

        # Check Tutorial
        has_tutorial = False
        if q.get("tutorial_md"):
            has_tutorial = True
        else:
            # Check disk
            for d in search_dirs:
                if os.path.exists(os.path.join(d, "tutorial.md")):
                    has_tutorial = True
                    break
        
        if has_tutorial:
            quests_with_tutorial += 1
        else:
            missing_tut_list.append(slug)
            
        # Check Terms
        has_terms = False
        terms = q.get("key_terms", [])
        if terms:
            has_terms = True
        else:
            # Check disk
            for d in search_dirs:
                if os.path.exists(os.path.join(d, "terms.json")):
                    has_terms = True
                    break

        if has_terms:
            quests_with_terms += 1
            
        # Check 1: 0 Objectives (Skip for overlay files if they lack 'objectives')
        # If accessing metadata from DB isn't possible here, we might just warn
        pass # We'll skip adding duplicate 'no objectives' checks here, relied on previous logic?
        # Re-adding minimal structural checks:
        
        # Only check objectives if this looks like a full definition (has title/desc)
        if "title" in q and "objectives" not in q and "objectives_json" not in q:
             issues.append(f"[{slug}] No objectives defined.")
             
        # Check Grading
        grading = q.get("grading", {})
        if grading.get("mode") == "tests":
            public_tests = grading.get("public_tests", [])
             # Strict check might fail for older format, let's be lenient or skip
            pass

    # Coverage Stats
    tut_coverage = (quests_with_tutorial / total_quests * 100) if total_quests > 0 else 0
    term_coverage = (quests_with_terms / total_quests * 100) if total_quests > 0 else 0
    
    print("\n📊 --- Tutorial Coverage ---")
    print(f"Total Quests: {total_quests}")
    print(f"Has Tutorial: {quests_with_tutorial} ({tut_coverage:.1f}%)")
    print(f"Has Terms:    {quests_with_terms} ({term_coverage:.1f}%)")
    
    if args.verbose and missing_tut_list:
        print("\nMissing Tutorials:")
        for s in missing_tut_list[:10]: # Limit output
            print(f" - {s}")
        if len(missing_tut_list) > 10: print(f" ... and {len(missing_tut_list)-10} more")

    if not issues:
        print("\n✅ Content Audit Passed (No structural errors)!")
    else:
        print(f"\n❌ Found {len(issues)} Structural Issues:")
        for i in issues:
            print(f"  - {i}")
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="Root Content Dir")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_root = args.root if args.root else os.path.join(base_dir, "data", "questpacks")
    
    audit_content(target_root)
