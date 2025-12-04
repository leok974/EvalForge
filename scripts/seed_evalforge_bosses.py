#!/usr/bin/env python
"""
Standalone script to seed core bosses for Boss QA.

Usage:
    python scripts/seed_evalforge_bosses.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main() -> int:
    from arcade_app.seed_bosses_core import seed_core_bosses
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    
    # Use sync engine for seeding
    db_url = os.getenv("DATABASE_URL", "postgresql://evalforge:evalforge@localhost:5432/evalforge")
    # Remove async driver if present
    db_url = db_url.replace("+asyncpg", "")
    
    engine = create_engine(db_url)
    
    try:
        with Session(engine) as session:
            seed_core_bosses(session)
        print("✅ Successfully seeded core bosses for Boss QA!")
        return 0
    except Exception as e:
        print(f"❌ Failed to seed bosses: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
