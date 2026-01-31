
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
                            quests.extend(data)
                        elif isinstance(data, dict) and "slug" in data:
                            quests.append(data)
                except Exception as e:
                    print(f"Error reading {path}: {e}")

    print(f"Found {len(quests)} quests.")
    
    issues = []
    
    for q in quests:
        slug = q.get("slug", "unknown")
        
        # Check 1: 0 Objectives
        objs = q.get("objectives_json", [])
        if not objs:
            issues.append(f"[{slug}] No objectives defined.")
            
        # Check 2: Tests but no Starter/Solution
        # Logic: If grading.mode == tests, we sort of expect starter/solution smoke config?
        # Or at least expected files?
        grading = q.get("grading", {})
        if grading.get("mode") == "tests":
            smoke = q.get("smoke", {})
            if not smoke.get("solution_workspace_files") and not smoke.get("solution_code"):
                 issues.append(f"[{slug}] Tests mode but no smoke solution defined.")
            
            # Check public tests exist
            public_tests = grading.get("public_tests", [])
            if not public_tests:
                 issues.append(f"[{slug}] Tests mode but no public_tests defined.")

    if not issues:
        print("✅ Content Audit Passed!")
    else:
        print(f"❌ Found {len(issues)} Issues:")
        for i in issues:
            print(f"  - {i}")
            
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pack_dir = os.path.join(base_dir, "data", "questpacks")
    audit_content(pack_dir)
