#!/usr/bin/env python3
"""
Database migration to add archive columns to questdefinition table.

This enables the legacy quest archival system by adding:
- is_archived: Boolean flag to mark archived quests
- archived_at: Timestamp when quest was archived
- archived_reason: Text description of why it was archived
"""

import asyncio
import sys
import os

# Add root to pythonpath
sys.path.append(os.getcwd())

from sqlalchemy import text
from arcade_app.database import get_session


async def run_migration():
    """Add archive columns to questdefinition table."""
    
    print("🚀 Starting archive columns migration...")
    
    async for session in get_session():
        try:
            # Add is_archived column
            print("   Adding is_archived column...")
            await session.execute(text("""
                ALTER TABLE questdefinition 
                ADD COLUMN IF NOT EXISTS is_archived BOOLEAN NOT NULL DEFAULT FALSE
            """))
            
            # Add archived_at column
            print("   Adding archived_at column...")
            await session.execute(text("""
                ALTER TABLE questdefinition 
                ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ NULL
            """))
            
            # Add archived_reason column
            print("   Adding archived_reason column...")
            await session.execute(text("""
                ALTER TABLE questdefinition 
                ADD COLUMN IF NOT EXISTS archived_reason TEXT NULL
            """))
            
            # Create index for performance
            print("   Creating index on is_archived...")
            await session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_questdefinition_is_archived 
                ON questdefinition (is_archived)
            """))
            
            await session.commit()
            
            print("✅ Migration completed successfully!")
            print()
            print("Archive columns added:")
            print("  - is_archived: BOOLEAN (default: FALSE)")
            print("  - archived_at: TIMESTAMPTZ (nullable)")
            print("  - archived_reason: TEXT (nullable)")
            print("  - Index: idx_questdefinition_is_archived")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(run_migration())
