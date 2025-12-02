import asyncio
import os
import sys
import frontmatter

# Setup Path
sys.path.append("/app")

from arcade_app.rag_helper import index_content
from arcade_app.database import init_db

# Codex directory - Fixed for Docker container structure
CODEX_DIR = "/app/data/codex"

async def run_ingestion():
    print("🚀 Starting Codex Ingestion...")
    
    # Ensure DB is initialized
    await init_db()
    
    if not os.path.exists(CODEX_DIR):
        print(f"⚠️ Codex directory not found: {CODEX_DIR}")
        return
    
    count = 0
    for root, _, files in os.walk(CODEX_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    post = frontmatter.load(path)
                    
                    # We index the Title + Tags + Content for context
                    title = post.metadata.get('title', 'Untitled')
                    tags = post.metadata.get('tags', [])
                    full_text = f"Title: {title}\nTags: {', '.join(tags) if tags else 'None'}\n\n{post.content}"
                    
                    doc_id = post.metadata.get("id", file.replace('.md', ''))
                    await index_content("codex", doc_id, full_text)
                    count += 1
                except Exception as e:
                    print(f"❌ Failed to index {file}: {e}")
    
    print(f"✨ Ingestion Complete! Indexed {count} codex entries.")

if __name__ == "__main__":
    asyncio.run(run_ingestion())
