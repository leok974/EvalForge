#!/usr/bin/env python3
"""
Seed the default avatar for user FK constraint.

This script ensures the AvatarDefinition table has the default 'default_user' avatar
that all new users reference.
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, create_engine
from arcade_app.models import AvatarDefinition, DEFAULT_AVATAR_ID

# Use the same DATABASE_URL pattern as other seed scripts
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://evalforge:evalforge@localhost:5432/evalforge")

# Convert async URL to sync for SQLModel
if "+asyncpg" in DATABASE_URL:
    SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")
else:
    SYNC_DATABASE_URL = DATABASE_URL

engine = create_engine(SYNC_DATABASE_URL, echo=False)


def main() -> None:
    print("🎭 Seeding default avatar...")
    
    with Session(engine) as session:
        existing = session.get(AvatarDefinition, DEFAULT_AVATAR_ID)
        if existing:
            print(f"✅ Default avatar '{DEFAULT_AVATAR_ID}' already exists.")
            print(f"   Name: {existing.name}")
            return

        avatar = AvatarDefinition(
            id=DEFAULT_AVATAR_ID,
            name="Default Adventurer",
            description="Fallback avatar for new users. A mysterious figure shrouded in starter gear.",
            visual_type="icon",
            visual_data="user",  # Lucide icon name
            rarity="common",
            required_level=1,
            is_active=True,
        )
        session.add(avatar)
        session.commit()
        print(f"✅ Seeded default avatar '{DEFAULT_AVATAR_ID}'.")
        print(f"   Name: {avatar.name}")
        print(f"   Description: {avatar.description}")


if __name__ == "__main__":
    main()
