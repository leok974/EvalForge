
import argparse
import json
import sys
import os

# Import service for DB access or just read files?
# Reading files is faster and works for unseeded content.
# But quests can be scattered.
# We'll use questpack_seed's find functionality to locate the file?
# Or just DB if seeded?
# User wants "Author preview", so unseeded is likely.
# Let's reuse find_json_files logic.

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.questpack_seed import find_json_files

def preview_quest(slug):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = find_json_files(root_dir)
    
    found_data = None
    found_file = None
    
    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Search inside
            candidates = []
            if isinstance(data, list): candidates = data
            elif isinstance(data, dict):
                if "packs" in data: candidates = data["packs"]
                elif "quests" in data: candidates = data["quests"]
                elif "slug" in data: candidates = [data]
            
            for q in candidates:
                if q.get("slug") == slug:
                    found_data = q
                    found_file = f_path
                    break
        except:
            continue
        if found_data: break
        
    if not found_data:
        print(f"❌ Quest '{slug}' not found in any known specs.")
        sys.exit(1)
        
    # Render Preview
    print(f"\n🔎 Preview: {found_data.get('title')} ({slug})")
    print(f"   Source: {found_file}\n")
    print("="*60)
    print(found_data.get("detailed_description", "(No description)"))
    print("="*60)
    print("\n🎯 Objectives:")
    for obj in found_data.get("objectives_json") or found_data.get("objectives") or []:
        print(f"  - [{obj.get('type')}] {obj.get('description')}")
        
    print("\n📂 Workspace:")
    ws = found_data.get("workspace") or {}
    print(f"  Entrypoint: {ws.get('entrypoint')}")
    if "files_from" in ws:
        print(f"  Hydration Source: {ws['files_from']} (Folder-based)")
    elif "files" in ws:
        print("  Files (Inline):")
        for f in ws["files"]:
            print(f"    - {f['path']}")
            
    print("\n⚙️ Grading Mode: " + str(found_data.get("grading", {}).get("mode", "run")))
    print("\n✅ Verification:")
    print(f"  Run 'python scripts/questpack_smoke.py --only {slug}' to test.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()
    preview_quest(args.slug)
