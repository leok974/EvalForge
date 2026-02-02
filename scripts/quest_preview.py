
import os
import sys
import json
import argparse
import glob

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils.validators import validate_tutorial_structure, validate_terms_schema, validate_codex_links

def find_quest_file(slug, root_dir):
    """Finds a quest JSON file by slug in likely locations."""
    # 1. docs/quests/{slug}/quest.json (Standard Authoring)
    p1 = os.path.join(root_dir, "docs", "quests", slug, "quest.json")
    if os.path.exists(p1): return p1
    
    # 2. data/questpacks/** (Pack based)
    search_pattern = os.path.join(root_dir, "data", "questpacks", "**", "*.json")
    for f in glob.glob(search_pattern, recursive=True):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for q in data:
                        if q.get("slug") == slug: return f
                elif isinstance(data, dict):
                    if data.get("slug") == slug: return f
        except:
            continue
            
    return None

def hydrate_preview(quest_path, slug):
    """Simulates hydration logic and returns the effective quest object."""
    base_dir = os.path.dirname(quest_path)
    
    # Load JSON
    with open(quest_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    # Extract specific quest if list
    target_data = raw_data
    if isinstance(raw_data, list):
        target_data = next((q for q in raw_data if q.get("slug") == slug), None)
    elif raw_data.get("slug") != slug:
        # Might be packs/quests envelope
        if "quests" in raw_data:
             target_data = next((q for q in raw_data["quests"] if q.get("slug") == slug), None)
    
    if not target_data:
        print(f"❌ Could not find slug '{slug}' inside {quest_path}")
        return None

    quest_obj = {
        "slug": slug,
        "title": target_data.get("title", "Unknown"),
        "tutorial_md": target_data.get("tutorial_md"),
        "key_terms": target_data.get("key_terms", []),
        "codex_references": target_data.get("codex_references", [])
    }

    # Hydrate Logic (Mirrors questpack_seed.py)
    # 1. Determine search dirs
    search_dirs = [base_dir]
    ws = target_data.get("workspace") or {}
    if "files_from" in ws:
        search_dirs.insert(0, os.path.join(base_dir, ws["files_from"]))
        
    print(f"🔎 searching for assets in: {[os.path.relpath(d) for d in search_dirs]}")

    # 2. tutorial.md
    if not quest_obj["tutorial_md"]:
        for d in search_dirs:
            tpath = os.path.join(d, "tutorial.md")
            if os.path.exists(tpath):
                print(f"   Found tutorial.md in {os.path.relpath(d)}")
                with open(tpath, "r", encoding="utf-8") as f:
                    quest_obj["tutorial_md"] = f.read()
                break

    # 3. terms.json
    if not quest_obj["key_terms"]:
        for d in search_dirs:
            tpath = os.path.join(d, "terms.json")
            if os.path.exists(tpath):
                print(f"   Found terms.json in {os.path.relpath(d)}")
                with open(tpath, "r", encoding="utf-8") as f:
                    quest_obj["key_terms"] = json.load(f)
                break
                
    # 4. Derive Refs
    if not quest_obj["codex_references"] and quest_obj["key_terms"]:
        derived = [t.get("codex_ref") for t in quest_obj["key_terms"] if t.get("codex_ref")]
        quest_obj["codex_references"] = list(set(derived))

    return quest_obj

def main():
    parser = argparse.ArgumentParser(description="Preview Quest Tutorial Content")
    parser.add_argument("--slug", required=True, help="Quest Slug")
    parser.add_argument("--root", default=os.getcwd(), help="Project Root")
    parser.add_argument("--check", action="store_true", help="Fail on errors")
    parser.add_argument("--show-md", action="store_true", help="Print Markdown content")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    
    args = parser.parse_args()
    
    # Find
    qpath = find_quest_file(args.slug, args.root)
    if not qpath:
        print(f"❌ Quest '{args.slug}' not found.")
        sys.exit(1)
        
    print(f"📁 Quest Source: {os.path.relpath(qpath, args.root)}")
    
    # Hydrate
    q_obj = hydrate_preview(qpath, args.slug)
    if not q_obj:
        sys.exit(1)
        
    # Validate
    # We pass the directory where the Hydrated assets 'effectively' live. 
    # For validation reuse, our validators look for files on disk.
    # But here we have loaded content. 
    # We might need to adapt validators or just manually validate the loaded obj.
    # The validators in utils/validators.py expect a directory path and look for files.
    # Since hydration happened from disk, we can pass the directory where we found the files?
    # Or just re-implement check here on the object.
    
    # Let's do object-level validation for preview
    errors = []
    
    # Tutorial
    if q_obj["tutorial_md"]:
        if len(q_obj["tutorial_md"]) < 50: errors.append("Tutorial too short")
        # Support both V1 (Mission Briefing) and V2 (Outcome)
        if "## Mission Briefing" not in q_obj["tutorial_md"] and "## Outcome" not in q_obj["tutorial_md"]:
            errors.append("Missing 'Mission Briefing' or 'Outcome' header")
    else:
        errors.append("No tutorial content found.")

    # Terms
    valid_refs = []
    if q_obj["key_terms"]:
        for item in q_obj["key_terms"]:
            ref = item.get("codex_ref")
            if ref:
                # Check resolution
                parts = ref.replace("codex:glossary/", "").split("/")
                if len(parts) >= 2:
                    rel_path = os.path.join("data", "codex", "glossary", *parts) + ".md"
                    abs_path = os.path.join(args.root, rel_path)
                    if not os.path.exists(abs_path):
                        errors.append(f"Broken Ref: {ref} -> {rel_path}")
                    else:
                        valid_refs.append(ref)
                else:
                    errors.append(f"Invalid Ref Format: {ref}")
    else:
         errors.append("No key terms found (or empty).")
         
    # Output
    if args.json:
        print(json.dumps(q_obj, indent=2))
        sys.exit(0 if not errors or not args.check else 1)
        
    print("\n--------- PREVIEW ---------")
    print(f"Title: {q_obj['title']}")
    print(f"Tutorial: {'✅ Loaded (' + str(len(q_obj['tutorial_md'])) + ' chars)' if q_obj['tutorial_md'] else '❌ Missing'}")
    print(f"Terms: {len(q_obj['key_terms'])} defined")
    print(f"Codex Refs: {len(q_obj['codex_references'])} derived, {len(valid_refs)} valid")
    
    if errors:
        print("\n⚠️  Validation Issues:")
        for e in errors:
            print(f"  - {e}")
            
    if args.show_md and q_obj["tutorial_md"]:
        print("\n--- MARKDOWN START ---")
        print(q_obj["tutorial_md"])
        print("--- MARKDOWN END ---")
        
    if args.check and errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
