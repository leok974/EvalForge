import os
from typing import List, Dict
from sqlmodel import select
from sqlalchemy import text
from arcade_app.database import get_session
from arcade_app.models import KnowledgeChunk

# Vertex AI Imports
import vertexai
from vertexai.language_models import TextEmbeddingModel

# Initialize Model (Lazy load recommended in prod, but fine here)
try:
    vertexai.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    # "text-embedding-004" is the current best-in-class for RAG
    embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    print("✅ Vertex AI Embeddings initialized")
except Exception as e:
    print(f"⚠️ Vertex AI Embeddings not available: {e}")
    embedding_model = None

async def generate_embedding(text_chunk: str) -> List[float]:
    """Generates a 768-dim vector for the input text."""
    if not embedding_model: 
        print("⚠️ Using mock embeddings (Vertex AI not configured)")
        return [0.0] * 768 # Mock fallback
    
    # Vertex API call
    embeddings = embedding_model.get_embeddings([text_chunk])
    return embeddings[0].values

async def index_content(source_type: str, source_id: str, content: str):
    """
    Splits content into chunks, embeds them, and saves to DB.
    """
    # 1. Simple Chunking (Split by paragraphs or chars)
    # For MVP, we'll split by double newline to grab paragraphs
    chunks = content.split("\n\n")
    
    async for session in get_session():
        # Clean up old entries for this source (Naive re-indexing)
        delete_stmt = text(
            "DELETE FROM knowledgechunk WHERE source_type = :stype AND source_id = :sid"
        )
        await session.execute(delete_stmt, {"stype": source_type, "sid": source_id})
        
        for i, chunk_text in enumerate(chunks):
            if not chunk_text.strip(): continue
            
            vector = await generate_embedding(chunk_text)
            
            entry = KnowledgeChunk(
                source_type=source_type,
                source_id=source_id,
                chunk_index=i,
                content=chunk_text,
                embedding=vector
            )
            session.add(entry)
        
        await session.commit()
        print(f"✅ Indexed {len(chunks)} chunks for {source_id}")

async def search_knowledge(query: str, limit: int = 3) -> List[str]:
    """
    Vector Search: Finds the most relevant text chunks for the query.
    """
    query_vec = await generate_embedding(query)
    
    async for session in get_session():
        # pgvector L2 distance operator (<->) or Cosine (<=>)
        # We generally use Cosine distance (<=>) for text embeddings
        statement = select(KnowledgeChunk).order_by(
            KnowledgeChunk.embedding.cosine_distance(query_vec)
        ).limit(limit)
        
        result = await session.execute(statement)
        chunks = result.scalars().all()
        return [r.content for r in chunks]
