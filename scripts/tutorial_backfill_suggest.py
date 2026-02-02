import os
import sys
import argparse
import glob
import json
# Local import fix: add scripts/ to path if running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.universe import load_universe_map

def find_quest_data(slug, root_dir):
    """Finds quest data and its file path by slug."""
    # 0. Load Universe Map for fallback metadata
    universe_map = load_universe_map(root_dir)
    fallback_data = universe_map.get(slug, {})

    # 1. search docs/quests keys
    p1 = os.path.join(root_dir, "docs", "quests", slug, "quest.json")
    if os.path.exists(p1):
        print(f"DEBUG: Found in docs: {p1}")
        with open(p1, "r", encoding="utf-8") as f:
            local = json.load(f)
            merged = {**fallback_data, **local}
            return merged, p1, "docs"

    # 2. search data/questpacks
    search_pattern = os.path.join(root_dir, "data", "questpacks", "**", "*.json")
    # print(f"DEBUG: Searching glob: {search_pattern}")
    files = glob.glob(search_pattern, recursive=True)
    # print(f"DEBUG: Found {len(files)} JSON files in questpacks")
    
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                found = None
                if isinstance(data, list):
                    for q in data:
                        if q.get("slug") == slug: 
                            found = q
                            break
                elif isinstance(data, dict):
                    s = data.get("slug")
                    # print(f"DEBUG: Checking {f} -> {s}")
                    if s == slug: 
                        found = data
                        
                if found:
                    print(f"DEBUG: Found in pack: {f}")
                    merged = {**fallback_data, **found}
                    return merged, f, "pack"
        except Exception as e:
            print(f"DEBUG: Error reading {f}: {e}")
            continue
            
    print(f"DEBUG: Quest {slug} not found in {len(files)} files checked.")
            
    return None, None, None

def generate_tutorial_draft(quest_data):
    """Generates a markdown draft based on quest metadata."""
    title = quest_data.get("title", "Untitled Quest")
    short_desc = quest_data.get("short_description", "Describe the core concept here.")
    
    objectives = quest_data.get("objectives", [])
    objectives = quest_data.get("objectives", [])
    obj_text = ""
    for o in objectives:
        if isinstance(o, dict):
            desc = o.get('description', 'Complete the objective')
        else:
            desc = str(o)
        obj_text += f"- {desc}\n"

    md = f"""# Mission Briefing
Welcome to **{title}**.

## 1. The Concept
{short_desc}

## 2. Key Term: [Term]
Define the most important term here.

## 3. The Details
Deep dive into the mechanics.

## 4. The Challenge
What you need to do:
{obj_text}

## 5. Pro Tip
Give a helpful tip relevant to this quest.
"""
    return md

def generate_terms_draft(quest_data, world_id):
    """Generates a terms.json draft based on tags or placeholders."""
    tags = quest_data.get("tags", [])
    terms = []
    
    # Use tags as potential terms if available
    potential_terms = tags if tags else ["term-1", "term-2"]
    
    # Limit to 3 max for start
    for t in potential_terms[:3]:
        slugified = t.lower().replace(" ", "-")
        terms.append({
            "term": t,
            "definition": "TODO: Add definition.",
            "codex_ref": f"codex:glossary/{world_id}/{slugified}"
        })
        
    return terms

def main():
    parser = argparse.ArgumentParser(description="Suggest Tutorial Content for Backfill")
    parser.add_argument("--slug", required=True, help="Quest Slug")
    parser.add_argument("--root", default=os.getcwd(), help="Project Root")
    parser.add_argument("--write", action="store_true", help="Write files to disk (only for docs/quests/ structure)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    
    args = parser.parse_args()
    
    q_data, q_path, q_type = find_quest_data(args.slug, args.root)
    
    if not q_data:
        print(f"❌ Quest '{args.slug}' not found.")
        sys.exit(1)
        
    print(f"✅ Found quest '{args.slug}' in {q_path} ({q_type})")
    
    # Generate Drafts
    tut_md = generate_tutorial_draft(q_data)
    terms_json = generate_terms_draft(q_data, q_data.get("world_id", "misc"))
    
    # Output
    if not args.write:
        print("\n--- DRAFT: tutorial.md ---")
        print(tut_md)
        print("\n--- DRAFT: terms.json ---")
        print(json.dumps(terms_json, indent=2))
        print("\n(Run with --write to save to disk)")
    else:
        # Determine strict output directory
        # If it's a "docs" quest, it's easy: same dir as quest.json
        # If it's a "pack" quest, it might be in a list file. 
        # For packs, we usually hydrate from 'files_from'.
        
        target_dir = os.path.dirname(q_path)
        
        # Check if 'files_from' exists in quest data workspace
        ws = q_data.get("workspace", {})
        if "files_from" in ws:
            # Resolving strictly relative to the quest.json location
            target_dir = os.path.join(target_dir, ws["files_from"])
            os.makedirs(target_dir, exist_ok=True)
            print(f"📂 Targeting workspace directory: {target_dir}")
        else:
             print(f"📂 Targeting directory: {target_dir}")

        # Write Tutorial
        t_path = os.path.join(target_dir, "tutorial.md")
        if os.path.exists(t_path) and not args.force:
            print(f"⚠️  Skipping tutorial.md (exists). Use --force to overwrite.")
        else:
            with open(t_path, "w", encoding="utf-8") as f:
                f.write(tut_md)
            print(f"💾 Wrote {t_path}")

        # Write Terms
        j_path = os.path.join(target_dir, "terms.json")
        if os.path.exists(j_path) and not args.force:
             print(f"⚠️  Skipping terms.json (exists). Use --force to overwrite.")
        else:
            with open(j_path, "w", encoding="utf-8") as f:
                json.dump(terms_json, f, indent=2)
            print(f"💾 Wrote {j_path}")

if __name__ == "__main__":
    main()
