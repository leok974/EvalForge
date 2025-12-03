import os
import asyncio
import frontmatter
from sqlmodel import select
from arcade_app.database import get_session
from arcade_app.models import KnowledgeChunk

CODEX_DIR = "data/codex/bosses"

async def ingest_boss_codex():
    print(f"🔍 Scanning Boss Codex at {CODEX_DIR}...")
    
    if not os.path.exists(CODEX_DIR):
        print(f"⚠️ Directory not found: {CODEX_DIR}")
        return

    async for session in get_session():
        count = 0
        for root, _, files in os.walk(CODEX_DIR):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        post = frontmatter.load(path)
                        
                        # Extract metadata
                        boss_id = post.metadata.get("boss_id")
                        tier = post.metadata.get("tier")
                        slug = post.metadata.get("slug", file.replace(".md", ""))
                        title = post.metadata.get("title", slug)
                        
                        if not boss_id:
                            print(f"⚠️ Skipping {file}: No boss_id found in frontmatter")
                            continue

                        # Prepare metadata JSON
                        meta = {
                            "boss_id": boss_id,
                            "tier": tier,
                            "slug": slug,
                            "title": title,
                            "world_id": post.metadata.get("world_id", "general"),
                            "tags": post.metadata.get("tags", [])
                        }

                        # Check if exists
                        stmt = select(KnowledgeChunk).where(
                            KnowledgeChunk.source_id == slug,
                            KnowledgeChunk.source_type == "codex"
                        )
                        existing = (await session.execute(stmt)).scalar_one_or_none()

                        if existing:
                            existing.content = post.content
                            existing.metadata_json = meta
                            session.add(existing)
                            print(f"  - Updated {slug}")
                        else:
                            new_chunk = KnowledgeChunk(
                                source_id=slug,
                                source_type="codex",
                                content=post.content,
                                metadata_json=meta
                            )
                            session.add(new_chunk)
                            print(f"  - Created {slug}")
                        
                        count += 1
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")
        
        await session.commit()
        print(f"✅ Ingested {count} boss codex entries.")

if __name__ == "__main__":
    asyncio.run(ingest_boss_codex())
