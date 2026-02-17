#!/usr/bin/env python3
"""Debug script to check python-ignition objectives in DB."""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.abspath('.'))

from arcade_app.database import get_sync_session
from arcade_app.models import QuestDefinition
import json

with get_sync_session() as db:
    quest = db.query(QuestDefinition).filter_by(slug='python-ignition').first()
    
    if not quest:
        print("❌ python-ignition not found in DB")
        sys.exit(1)
    
    print(f"✅ Found quest: {quest.slug}")
    print(f"   Title: {quest.title}")
    print(f"   Objectives JSON:")
    print(json.dumps(quest.objectives_json, indent=2))
    print(f"\n   Runtime Rules JSON:")
    print(json.dumps(quest.runtime_rules_json, indent=2))
