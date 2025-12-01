import pytest
import json
import os
import sys
from unittest.mock import patch, mock_open, MagicMock, AsyncMock
from sqlmodel import select
from arcade_app.models import KnowledgeChunk
from arcade_app.rag_helper import index_content

# Add root path to import scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from scripts.seed_meta_codex import META_DOCS, seed

# Mark async tests
pytestmark = pytest.mark.asyncio

def test_meta_world_registered():
    """Verify 'world-evalforge' is in the worlds.json config."""
    with open("data/worlds.json", "r", encoding="utf-8") as f:
        worlds = json.load(f)
    
    meta_world = next((w for w in worlds if w["id"] == "world-evalforge"), None)
    
    assert meta_world is not None
    assert meta_world["name"] == "EvalForge System"
    assert "THE CONSTRUCT" in meta_world["narrative_config"]["alias"]
    assert "The Architect" in meta_world["narrative_config"]["role"]

def test_seed_script_writes_files():
    """Verify the seed script attempts to write the Golden Copy files."""
    # Mock file writing to avoid disk spam during tests
    m = mock_open()
    
    with patch("builtins.open", m), patch("os.makedirs"):
        seed()
        
        # Verify it wrote one file per entry in META_DOCS
        assert m.call_count == len(META_DOCS)
        
        # Check content of one write
        handle = m()
        # args[0] is the content written. Check for KAI.
        written_content = [call.args[0] for call in handle.write.call_args_list]
        kai_content = next((c for c in written_content if "KAI (Quest Protocol)" in c), None)
        
        assert kai_content is not None
        assert "Mission Control" in kai_content
        assert "world-evalforge" in kai_content

async def test_meta_content_ingestion(db_session):
    """
    Verify that a Meta-Codex entry can be successfully indexed into pgvector.
    """
    # 1. Create dummy meta-content
    doc_id = "entity-zero.md"
    content = """---
id: entity-zero
title: ZERO
world: world-evalforge
---
# Identity
ZERO is the System Arbiter.
"""
    
    # 2. Mock Embedding Model (return random vector)
    mock_vector = [0.1] * 768
    
    # Patch get_session to use our test db_session
    async def mock_get_session():
        yield db_session

    with patch("arcade_app.rag_helper.generate_embedding", new_callable=AsyncMock) as mock_embed, \
         patch("arcade_app.rag_helper.get_session", side_effect=mock_get_session):
        mock_embed.return_value = mock_vector
        
        # 3. Run Indexer
        await index_content(
            source_type="codex", 
            source_id=doc_id, 
            content=content
        )
        
        # 4. Verify DB
        chunks = (await db_session.execute(
            select(KnowledgeChunk).where(KnowledgeChunk.source_id == doc_id)
        )).scalars().all()
        
        assert len(chunks) > 0
        assert chunks[0].source_type == "codex"
        assert "System Arbiter" in chunks[0].content
