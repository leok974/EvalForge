#!/usr/bin/env python3
"""
Test: Ensure python-ignition has objectives after seeding.
"""

def test_python_ignition_has_objectives():
    """Verify python-ignition has objectives configured in DB."""
    import sys
    import os
    sys.path.insert(0, os.path.abspath('.'))
    
    from arcade_app.database import get_session
    from arcade_app.models import QuestDefinition
    
    with next(get_session()) as db:
        quest = db.query(QuestDefinition).filter_by(slug='python-ignition').first()
        
        assert quest is not None, "python-ignition quest not found in database"
        assert quest.objectives_json is not None, "python-ignition has no objectives_json"
        assert len(quest.objectives_json) >= 1, f"python-ignition has {len(quest.objectives_json)} objectives, expected >= 1"
        
        # Verify specific objectives
        obj_ids = [obj['id'] for obj in quest.objectives_json]
        assert 'obj_runs' in obj_ids, "Missing 'obj_runs' objective"
        assert 'obj_output' in obj_ids, "Missing 'obj_output' objective"
        
        print(f"✅ python-ignition has {len(quest.objectives_json)} objectives: {obj_ids}")
        return True

if __name__ == "__main__":
    try:
        test_python_ignition_has_objectives()
        print("\n✅ TEST PASSED")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
