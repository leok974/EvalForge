import json
import os

QUESTPACKS = [
    "data/questpacks/foundry_python.json",
    "data/questpacks/python_systems.json"
]

def load_questpack(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def dump_file(label, path):
    if not os.path.exists(path):
        return f"### {label}\n*(File not found: {path})*\n"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return f"### {label}\n```\n{content}\n```\n"

def main():
    print("# Python Refinement Source Packets\n")
    
    seen_slugs = set()
    
    for qp_path in QUESTPACKS:
        if not os.path.exists(qp_path):
            continue
            
        quests = load_questpack(qp_path)
        for quest in quests:
            slug = quest.get("slug")
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            
            print(f"## Quest: {slug}")
            print(f"**Title:** {quest.get('title')}")
            print(f"**Description:** {quest.get('description')}\n")
            
            # Determine quest directory
            # If files_from is present in workspace config, use that.
            # Otherwise assume data/quests/{slug}
            
            ws_config = quest.get("workspace", {})
            files_from = ws_config.get("files_from")
            
            if files_from:
                # files_from is usually relative to the questpack json, which is data/questpacks/
                # so ../quests/{slug}/workspace
                # We need to resolve it relative to CWD
                # path is data/questpacks/../quests/{slug}/workspace
                # normalized: data/quests/{slug}/workspace
                
                # Check if it starts with ../
                if files_from.startswith("../"):
                    quest_dir = os.path.normpath(os.path.join(os.path.dirname(qp_path), files_from, ".."))
                else:
                     quest_dir = f"data/quests/{slug}"
            else:
                 quest_dir = f"data/quests/{slug}"
            
            # 1. README
            readme_path = os.path.join(quest_dir, "workspace", "README.md")
            print(dump_file("1) README.md", readme_path))
            
            # 2. Starter Code (task.py)
            starter_path = os.path.join(quest_dir, "workspace", "task.py")
            if not os.path.exists(starter_path):
                 starter_path = os.path.join(quest_dir, "workspace", "task.txt") # Fallback
            
            print(dump_file("2) Starter Code", starter_path))
            
            # 3. Test File
            # Look for grading folder
            grading_dir = os.path.join(quest_dir, "grading")
            test_file = None
            
            if os.path.exists(grading_dir):
                # Try to find a python test file
                for root, dirs, files in os.walk(grading_dir):
                    for file in files:
                        if file.endswith(".py") and "test" in file:
                            test_file = os.path.join(root, file)
                            break
                    if test_file:
                        break
            
            if test_file:
                print(dump_file(f"3) Test File ({os.path.basename(test_file)})", test_file))
            else:
                print("### 3) Test File\n*(No explicit test file found in grading directory. Likely implicit runtime check via exit code/stdout.)*\n")
            
            print("---\n")

if __name__ == "__main__":
    main()
