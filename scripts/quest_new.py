
import argparse
import os
import json
import sys

def create_quest_scaffold(args):
    # 1. Determine Target Directory
    # Convention: docs/quests/{slug}/quest.json
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_base = os.path.join(root_dir, "docs", "quests", args.slug)
    
    if os.path.exists(target_base):
        print(f"❌ Error: directory {target_base} already exists.")
        sys.exit(1)
        
    os.makedirs(target_base)
    os.makedirs(os.path.join(target_base, "starter"))
    os.makedirs(os.path.join(target_base, "solution"))
    
    # 2. Create Workspace Files
    # Starter
    starter_entry = "main.py" if args.language == "python" else "main.ts"
    with open(os.path.join(target_base, "starter", starter_entry), "w", encoding="utf-8") as f:
        f.write("# Starter Code\n\ndef solution():\n    pass\n")
        
    # Solution
    with open(os.path.join(target_base, "solution", starter_entry), "w", encoding="utf-8") as f:
        f.write("# Solution Code\n\ndef solution():\n    return 42\n")

    # Tests (if applicable)
    if args.kind == "tests" and args.language == "python":
         with open(os.path.join(target_base, "starter", "test_public.py"), "w", encoding="utf-8") as f:
             f.write("import unittest\nfrom main import solution\n\nclass TestPublic(unittest.TestCase):\n    def test_basic(self):\n        self.assertEqual(solution(), 42)\n")

    # 3. Generate Quest JSON
    quest_data = {
        "slug": args.slug,
        "title": args.title,
        "language": args.language,
        "world_id": args.world,
        "track_id": args.track,
        "order_index": 1, # TODO: auto-detect max + 1
        "short_description": "A generated quest description.",
        "detailed_description": "Use markdown here.\n\n# Objectives\n- Solve the problem.",
        "objectives": [
            {
                "id": "obj_1",
                "description": "Implement the solution.",
                "type": "test_pass" if args.kind == "tests" else "output_match",
                "matcher": ".*" if args.kind == "output" else None
            }
        ],
        "grading": {
            "mode": args.kind
        },
        "workspace": {
            "entrypoint": starter_entry,
            "files_from": "./starter"
        },
        "smoke": {
            "solution_workspace_files": [] # Could hydrate solution too? 
            # We don't have hydration logic for smoke config yet in seed_all, but we can implement it or manually point?
            # Actually, `smoke` config usually expects content string or file object list in JSON. 
            # Ideally we'd support `files_from` in smoke too, but for now let's just leave it empty or use manual setup
        }
    }
    
    # Write JSON
    json_path = os.path.join(target_base, "quest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(quest_data, f, indent=4)
        
    print(f"✅ Quest scaffold created at: {target_base}")
    print(f"   - {json_path}")
    print(f"   - starter/{starter_entry}")
    print("👉 Next: Edit the files, then run 'python scripts/dev_validate_all.py' to verify.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new quest")
    parser.add_argument("--world", required=True, help="World ID (e.g. foundry)")
    parser.add_argument("--track", required=True, help="Track ID")
    parser.add_argument("--slug", required=True, help="Quest Slug (unique)")
    parser.add_argument("--title", required=True, help="Quest Title")
    parser.add_argument("--language", default="python", choices=["python", "typescript", "java"], help="Language")
    parser.add_argument("--kind", default="tests", choices=["tests", "output"], help="Grading mode")
    
    args = parser.parse_args()
    create_quest_scaffold(args)
