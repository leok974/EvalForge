#!/usr/bin/env python3
"""Fix hello-variable objectives in DB."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from arcade_app.models import QuestDefinition
from arcade_app.config import DATABASE_URL

# Sync URL
sync_url = DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(sync_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
try:
    quest = db.query(QuestDefinition).filter_by(slug='hello-variable').first()
    
    if not quest:
        print("❌ hello-variable not found")
        sys.exit(1)
    
    # Fix objectives
    quest.objectives_json = [
        {
            "id": "obj_var_energy",
            "kind": "ast",
            "title": "Define variable 'energy'",
            "rule": {
                "kind": "ast",
                "must_assign_variable": "energy"
            },
            "why": "Practice variable assignment"
        }
    ]
    
    db.commit()
    print("✅ Updated hello-variable objectives")
    print(f"   Objectives: {quest.objectives_json}")

finally:
    db.close()
