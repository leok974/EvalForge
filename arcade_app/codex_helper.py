import os
import frontmatter
from typing import List, Dict, Optional
from sqlalchemy import select
from arcade_app.models import KnowledgeChunk

CODEX_DIR = "docs/codex"

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
                    world = post.metadata.get("world", "general")
                    
                    # Calculate ID from relative path if not in frontmatter
                    rel_path = os.path.relpath(path, CODEX_DIR)
                    default_id = os.path.splitext(rel_path)[0].replace(os.path.sep, "/")
                    
                    index.append({
                        "id": post.metadata.get("id", default_id),
                        "title": post.metadata.get("title", "Untitled Entry"),
                        "world": world,
                        "world_id": world, # Alias for frontend consistency
                        "tags": post.metadata.get("tags", []),
                        "source": post.metadata.get("source", "core"),
                        "section": rel_path.split(os.path.sep)[0] if os.path.sep in rel_path else "general"
                        # We don't send content here to keep the list lightweight
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing Codex entry {file}: {e}")
    
    return index

def build_codex_index() -> Dict:
    """
    Builds a structured index for the Codex Library view.
    Returns: { "sections": [ { "world":Str, "section":Str, "pages": [ ... ] } ] }
    """
    flat_index = index_codex()
    
    # Group by (world, section)
    grouped = {}
    
    for entry in flat_index:
        key = (entry.get("world", "general"), entry.get("section", "general"))
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)
        
    # Format for frontend
    sections = []
    for (world, section), pages in grouped.items():
        sections.append({
            "world": world,
            "section": section,
            "pages": sorted(pages, key=lambda x: x["title"])
        })
        
    # Sort sections by World then Section
    sections.sort(key=lambda x: (x["world"], x["section"]))
    
    return {"sections": sections}

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
                    
                    rel_path = os.path.relpath(path, CODEX_DIR)
                    default_id = os.path.splitext(rel_path)[0].replace(os.path.sep, "/")
                    
                    current_id = post.metadata.get("id", default_id)
                    
                    # Robust ID matching: Match if IDs are equal, or if they match after normalization (strip codex:)
                    # This handles cases where frontmatter has "codex:foo" but request is for "foo"
                    
                    cid_norm = current_id.replace("codex:", "")
                    eid_norm = entry_id.replace("codex:", "")
                    
                    if current_id == entry_id or cid_norm == eid_norm:
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
