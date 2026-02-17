#!/usr/bin/env python3
"""Check if python-ignition has objectives configured."""

from arcade_app.database import get_session
from arcade_app.models import QuestDefinition

with next(get_session()) as db:
    q = db.query(QuestDefinition).filter_by(slug='python-ignition').first()
    if q:
        print(f"Quest: {q.slug}")
        print(f"Objectives: {q.objectives_json}")
        print(f"Runtime rules: {q.runtime_rules_json}")
    else:
        print("Quest not found")
    
    # Find quests with objectives
    print("\n--- Quests with objectives ---")
    quests = db.query(QuestDefinition).limit(20).all()
    for quest in quests:
        if quest.objectives_json:
            print(f"{quest.slug}: {len(quest.objectives_json)} objectives")
