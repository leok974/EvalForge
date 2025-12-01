import os
import frontmatter
from typing import List, Dict, Optional
from sqlalchemy import select
from arcade_app.models import KnowledgeChunk

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


async def load_codex_entry_by_id(session, codex_id: str) -> Optional[dict]:
    """
    Load a codex entry by ID from the knowledge base.
    
    Args:
        session: Database session
        codex_id: Codex entry identifier (e.g. "boss-reactor-core")
    
    Returns:
        Dict with title, summary, and body_markdown, or None if not found
    """
    # Query for knowledge chunks matching this codex_id
    stmt = select(KnowledgeChunk).where(
        KnowledgeChunk.source_id == codex_id # Changed doc_id to source_id based on models.py
    ).limit(1)
    
    result = await session.execute(stmt)
    chunk = result.scalar_one_or_none()
    
    if not chunk:
        return None
    
    return {
        "id": chunk.source_id,
        "title": "Codex Entry", # Metadata might be lost in chunking, fallback
        "summary": "",
        "body_markdown": chunk.content,
        "tags": "",
    }
