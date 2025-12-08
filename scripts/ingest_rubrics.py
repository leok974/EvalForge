import asyncio
import json
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select, delete

from arcade_app.database import engine
from arcade_app.models import KnowledgeChunk 

BASE_DOCS = Path("d:/EvalForge/rubrics") # Index files live here
BASE_RUBRICS = Path("d:/EvalForge") # Rubric files live here (rubrics/...)

RUBRIC_INDEXES = [
    "boss_rubric_index.json",
    "boss_rubric_index.world-git.json",
    "boss_rubric_index.world-sql.json",
    "boss_rubric_index.world-ml.json",
    "boss_rubric_index.world-python.json"
]
async def ingest_rubric_entry(session, entry, world_slug):
    rubric_id = entry.get("rubric_id", entry.get("id"))
    file_path = BASE_RUBRICS / entry["path"]

    if not file_path.exists():
         print(f"⚠️ File not found: {file_path}")
         return

    content_json = file_path.read_text(encoding="utf-8")
    
    print(f"  - ⚖️ Ingesting Rubric: {rubric_id}")
    
    # Clean existing
    stmt = delete(KnowledgeChunk).where(
        (KnowledgeChunk.source_id == rubric_id) & 
        (KnowledgeChunk.source_type == "boss_rubric")
    )
    await session.execute(stmt)
    
    # Insert as Chunk
    chunk = KnowledgeChunk(
        source_type="boss_rubric",
        source_id=rubric_id,
        chunk_index=0,
        content=content_json, # Storing RAW JSON as content
        metadata_json={
            "title": entry["title"],
            "boss_id": rubric_id,
            "world_slug": world_slug,
            "tags": entry.get("tags", [])
        },
        embedding=[0.0] * 768 # Placeholder zero vector
    )
    session.add(chunk)

async def ingest_rubrics():
    print("⚖️ Ingesting Boss Rubrics...")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        for index_file in RUBRIC_INDEXES:
            path = BASE_DOCS / index_file
            if not path.exists():
                print(f"⚠️ Index not found: {index_file}"); continue
                
            index_data = json.loads(path.read_text(encoding="utf-8"))
            world_slug = index_data.get("world_slug", "unknown")
            
            entries = index_data.get("rubrics", index_data.get("items", []))
            for entry in entries:
                await ingest_rubric_entry(session, entry, world_slug)
                
        await session.commit()
    print("✅ Rubric Ingestion Complete.")

if __name__ == "__main__":
    import sys
    sys.path.append("d:/EvalForge")
    asyncio.run(ingest_rubrics())
