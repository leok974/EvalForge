
import os
import json
import frontmatter
from pathlib import Path

CODEX_ROOT = Path("docs/codex")
QUESTS_ROOT = Path("docs/quests")

def get_codex_redirects():
    """Build a map of RedirectID -> TargetID."""
    redirects = {}
    for file_path in CODEX_ROOT.rglob("*.md"):
        try:
            post = frontmatter.load(file_path)
            if post.metadata.get("redirect_to"):
                # Normalize IDs (strip codex:)
                src_id = post.metadata.get("id")
                if not src_id:
                     rel_path = file_path.relative_to(CODEX_ROOT)
                     src_id = str(rel_path.with_suffix("")).replace(os.sep, "/")
                
                src_id = src_id.replace("codex:", "")
                target_id = post.metadata["redirect_to"].replace("codex:", "")
                
                redirects[src_id] = target_id
        except:
            pass
    return redirects

def optimize_quests():
    redirects = get_codex_redirects()
    print(f"Loaded {len(redirects)} redirects.")
    
    updated_count = 0
    
    for term_file in QUESTS_ROOT.rglob("terms.json"):
        try:
            with open(term_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            original_json = json.dumps(data)
            modified = False
            
            # Helper to process a ref string
            def process_ref(ref):
                if not ref.startswith("codex:"):
                    return ref, False
                
                term_id = ref.replace("codex:", "")
                if term_id in redirects:
                    # Resolve recursively?
                    # Audit script resolves recursively. Let's do 1 hop for safety or loop until resolved.
                    # Since audit passed, loops are unlikely but let's be safe.
                    curr = term_id
                    for _ in range(5):
                        if curr in redirects:
                            curr = redirects[curr]
                        else:
                            break
                    
                    new_ref = f"codex:{curr}"
                    if new_ref != ref:
                        return new_ref, True
                return ref, False

            # Handle Dict vs List format
            if isinstance(data, dict):
                new_refs = []
                for ref in data.get("codex_references", []):
                    new_ref, changed = process_ref(ref)
                    new_refs.append(new_ref)
                    if changed:
                        print(f"  Fixed {ref} -> {new_ref}")
                        modified = True
                data["codex_references"] = new_refs
                
            elif isinstance(data, list):
                for item in data:
                    if "codex_ref" in item:
                        new_ref, changed = process_ref(item["codex_ref"])
                        if changed:
                            print(f"  Fixed {item['codex_ref']} -> {new_ref}")
                            item["codex_ref"] = new_ref
                            modified = True

            if modified:
                # Format JSON nicely
                with open(term_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                updated_count += 1
                # print(f"Updated {term_file}")
                
        except Exception as e:
            print(f"Failed to process {term_file}: {e}")

    print(f"Optimized {updated_count} quest files.")

if __name__ == "__main__":
    optimize_quests()
