import json
import os
import sys

def main():
    if not os.path.exists("codex_orphans.json"):
        print("No codex_orphans.json found. Run validate_tutorials.py first.")
        return

    with open("codex_orphans.json", "r") as f:
        orphans = json.load(f)

    print(f"Loaded {len(orphans)} orphans to delete.")
    
    root_dir = os.getcwd()
    
    deleted_count = 0
    for ref in orphans:
        # ref format: codex:glossary/{path}
        # file format: data/codex/glossary/{path}.md
        
        if not ref.startswith("codex:glossary/"):
            print(f"Skipping malformed ref: {ref}")
            continue
            
        rel_path = ref.replace("codex:glossary/", "") + ".md"
        full_path = os.path.join(root_dir, "data", "codex", "glossary", rel_path)
        
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"Deleted: {rel_path}")
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {full_path}: {e}")
        else:
            print(f"File not found (already gone?): {full_path}")
            
    print(f"\nCleanup complete. Deleted {deleted_count} files.")

if __name__ == "__main__":
    main()
