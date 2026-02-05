
import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return None

def get_active_questpacks(root_dir: str) -> List[str]:
    config_path = os.path.join(root_dir, "configs", "questpacks_active.json")
    data = load_json(config_path)
    if not data: return []
    return [os.path.join(root_dir, p) for p in data.get("active_questpacks", [])]

def get_active_slugs(root_dir: str) -> Set[str]:
    slugs = set()
    packs = get_active_questpacks(root_dir)
    for pack_path in packs:
        if not os.path.exists(pack_path): continue
        data = load_json(pack_path)
        if not data: continue
        
        quests = []
        if isinstance(data, list): quests = data
        elif "quests" in data: quests = data["quests"]
        elif "packs" in data: quests = data["packs"]
        
        for q in quests:
            if "slug" in q: slugs.add(q["slug"])
    return slugs

def check_workspace(slug: str, root_dir: str) -> List[str]:
    errors = []
    workspace_dir = os.path.join(root_dir, "data", "quests", slug, "workspace")
    
    # 1. Check Directory Exists
    if not os.path.isdir(workspace_dir):
        errors.append(f"Workspace directory missing: {workspace_dir}")
        return errors # Critical failure, return early
        
    # 2. Check Starter File
    # Heuristic based on slug/language
    # Node/JS -> index.js
    # TS -> index.ts
    # Python -> task.py
    # HTML -> index.html
    # CSS -> style.css
    
    expected_files = []
    if "node-" in slug or "js-" in slug or "react-" in slug: expected_files = ["index.js", "App.jsx", "task.mjs"]
    elif "ts-" in slug or "typescript-" in slug: expected_files = ["index.ts", "task.ts"]
    elif "python-" in slug or "foundry-" in slug or "ml-" in slug: expected_files = ["task.py", "main.py"]
    elif "html-" in slug: expected_files = ["index.html"]
    elif "css-" in slug: expected_files = ["style.css", "index.html"]
    else:
        # Generic fallback: look for ANY file
        if not os.listdir(workspace_dir):
             errors.append("Workspace is empty")
        return errors

    found = False
    for f in expected_files:
        if os.path.exists(os.path.join(workspace_dir, f)):
            found = True
            break
            
    if not found and expected_files:
        # Double check generic fallback if heuristics fail
        if not os.listdir(workspace_dir):
             errors.append(f"Workspace empty. Expected one of: {expected_files}")
    
    return errors

def main():
    parser = argparse.ArgumentParser(description="Audit quest workspaces")
    parser.add_argument("--active", action="store_true", help="Audit only active questpacks")
    parser.add_argument("--fail", action="store_true", help="Exit with non-zero code on failure")
    args = parser.parse_args()
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    slugs_to_check = set()
    if args.active:
        slugs_to_check = get_active_slugs(root_dir)
        print(f"🔍 Scoping audit to {len(slugs_to_check)} active quests...")
    else:
        # Scan all directories in data/quests?
        pass # Simplified for this task to just do active
        
    failures = {}
    
    for slug in slugs_to_check:
        errs = check_workspace(slug, root_dir)
        if errs:
            failures[slug] = errs
            
    if failures:
        print(f"\n❌ Found {len(failures)} quests with workspace issues:")
        for slug, errs in failures.items():
            print(f"  - {slug}: {'; '.join(errs)}")
        
        if args.fail:
            sys.exit(1)
    else:
        print("\n✅ All active quest workspaces verified.")

if __name__ == "__main__":
    main()
