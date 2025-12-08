import asyncio
import json
import os
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete

# App Imports
from arcade_app.database import engine
from arcade_app.models import KnowledgeChunk

BASE_DOCS = Path("d:/EvalForge/docs")
BASE_CODEX = Path("d:/EvalForge") # Relative paths in index start with codex/...

CODEX_INDEXES = [
    "boss_codex_index.json", # This might not exist, but loop handles missing
    "boss_codex_index.world-git.json",
    "boss_codex_index.world-sql.json",
    "boss_codex_index.world-ml.json",
    "boss_codex_index.world-python.json"
]
async def ingest_codex_entry(session, entry, world_slug):
    codex_id = entry.get("boss_id", entry.get("id"))
    file_path = BASE_CODEX / entry["path"]
    
    if not file_path.exists():
        print(f"⚠️ File not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    
    print(f"  - 📜 Ingesting Codex: {codex_id}")
    
    # 1. Clean existing chunks for this codex_id
    stmt = delete(KnowledgeChunk).where(
        (KnowledgeChunk.source_id == codex_id) & 
        (KnowledgeChunk.source_type == "boss_codex")
    )
    await session.execute(stmt)
    
    # 2. Chunk it (Simulated simple chunking for now, entire doc as one chunk often okay for small codex)
    # For actual RAG we might want smaller chunks.
    
    chunk = KnowledgeChunk(
        source_type="boss_codex",
        source_id=codex_id,
        chunk_index=0,
        content=content,
        metadata_json={
            "title": entry["title"],
            "boss_id": codex_id,
            "world_slug": world_slug,
            "tags": entry.get("tags", [])
        },
        embedding=[0.0] * 768 # Placeholder zero vector to satisfy PGVector constraint
    )
    session.add(chunk)

async def ingest_codexes():
    print("📚 Ingesting Codex Entries...")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        for index_file in CODEX_INDEXES:
            path = BASE_DOCS / index_file
            if not path.exists():
                print(f"⚠️ Index not found: {index_file}"); continue
                
            index_data = json.loads(path.read_text(encoding="utf-8"))
            world_slug = index_data.get("world_slug", "unknown")
            
            entries = index_data.get("boss_codex", index_data.get("items", []))
            for entry in entries:
                try:
                    await ingest_codex_entry(session, entry, world_slug)
                except Exception as e:
                    print(f"❌ ERROR processing entry {entry.get('id')}: {e}")
                    import traceback
                    traceback.print_exc()
        
        await session.commit()
    print("✅ Codex Ingestion Complete.")

if __name__ == "__main__":
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(ingest_codexes())
