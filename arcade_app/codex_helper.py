import os
import frontmatter
from typing import List, Dict, Optional

CODEX_DIR = "data/codex"

def index_codex() -> List[Dict]:
    """
    Scans the data/codex directory and returns a list of metadata summaries.
    Used for the list view/search in the UI.
    """
    index = []
    if not os.path.exists(CODEX_DIR):
        print(f"⚠️ Codex directory not found at {CODEX_DIR}")
        return []

    # Walk through all files in the directory
    for root, _, files in os.walk(CODEX_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    # Parse Frontmatter
                    post = frontmatter.load(path)
                    
                    # Create summary entry
                    index.append({
                        "id": post.metadata.get("id", file.replace(".md", "")),
                        "title": post.metadata.get("title", "Untitled Entry"),
                        "world": post.metadata.get("world", "general"),
                        "tags": post.metadata.get("tags", []),
                        # We don't send content here to keep the list lightweight
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing Codex entry {file}: {e}")
    
    return index

def get_codex_entry(entry_id: str) -> Optional[Dict]:
    """
    Retrieves the full content and metadata for a specific entry ID.
    """
    for root, _, files in os.walk(CODEX_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    post = frontmatter.load(path)
                    current_id = post.metadata.get("id", file.replace(".md", ""))
                    
                    if current_id == entry_id:
                        return {
                            "metadata": post.metadata,
                            "content": post.content
                        }
                except:
                    continue
    return None
