#!/usr/bin/env python
"""
Debug script to test SQLModel table creation outside of FastAPI startup.

This will help identify if the issue is with:
- Model registration
- Engine configuration
- Async create_all execution

Usage:
    python scripts/debug_sqlmodel_create_all.py
"""
import asyncio
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import SQLModel
from sqlalchemy import text
from arcade_app.database import engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    logger.info("=" * 60)
    logger.info("SQLModel Table Creation Debug")
    logger.info("=" * 60)
    
    # 1. Import models to ensure they're registered
    logger.info("\n1. Importing models...")
    from arcade_app import models
    
    # 2. Check metadata
    logger.info("\n2. Checking SQLModel metadata...")
    all_tables = list(SQLModel.metadata.tables.keys())
    logger.info(f"   Total tables in metadata: {len(all_tables)}")
    logger.info(f"   First 10 tables: {all_tables[:10]}")
    logger.info(f"   'bossdefinition' in metadata: {'bossdefinition' in all_tables}")
    
    # 3. Check engine URL
    logger.info("\n3. Checking engine configuration...")
    logger.info(f"   Engine URL: {engine.url}")
    logger.info(f"   Engine dialect: {engine.dialect.name}")
    
    # 4. Run create_all
    logger.info("\n4. Running create_all...")
    async with engine.begin() as conn:
        # Enable pgvector extension first (required for KnowledgeChunk.embedding)
        logger.info("   Enabling pgvector extension...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        logger.info("   Running SQLModel.metadata.create_all...")
        await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("   create_all completed")
        
        # 5. Verify tables in database
        logger.info("\n5. Querying tables from database...")
        result = await conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema='public' ORDER BY table_name"
            )
        )
        db_tables = [row[0] for row in result]
        logger.info(f"   Total tables in DB: {len(db_tables)}")
        logger.info(f"   Tables in DB: {db_tables}")
        logger.info(f"   'bossdefinition' in DB: {'bossdefinition' in db_tables}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Debug complete!")
    logger.info("=" * 60)
    
    if 'bossdefinition' in db_tables:
        logger.info("✅ SUCCESS: bossdefinition table created!")
        return 0
    else:
        logger.error("❌ FAILURE: bossdefinition table NOT created")
        logger.error("   Metadata had it: %s", 'bossdefinition' in all_tables)
        logger.error("   DB has it: False")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
