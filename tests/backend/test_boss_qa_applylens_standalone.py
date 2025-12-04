#!/usr/bin/env python
"""
Standalone test for ApplyLens boss QA system (no server required).
Tests the full ZERO -> rubric -> scoring pipeline in mock mode.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Enable mock mode
os.environ["EVALFORGE_MOCK_GRADING"] = "1"


def test_applylens_boss_qa():
    """Test the boss QA system end-to-end."""
    from arcade_app.database import init_db, get_session
    from arcade_app.models import Profile
    from arcade_app.boss_qa_applylens import run_applylens_boss_qa
    from sqlalchemy.orm import Session
    
    print("=" * 60)
    print("ApplyLens Boss QA - Standalone Test")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_db()
    
    # Get DB session
    session_gen = get_session()
    db: Session = next(session_gen)
    
    try:
        # Create test profile
        print("2. Creating test profile...")
        test_profile = Profile(
            id="test_user_qa",
            display_name="QA Test User",
            integrity=100,
            xp=0,
            level=5,
            flags={}
        )
        db.add(test_profile)
        db.commit()
        db.refresh(test_profile)
        
        # Run QA
        print("3. Running ApplyLens boss QA...")
        print("   - Testing Inbox Maelstrom (runtime)")
        print("   - Testing Intent Oracle (agent)")
        
        report = run_applylens_boss_qa(
            db=db,
            player=test_profile,
            min_score_runtime=60,
            min_score_agent=60,
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("QA REPORT")
        print("=" * 60)
        print(f"Project: {report.project_slug}")
        print(f"Overall Pass: {report.overall_pass}")
        print()
        
        for result in report.results:
            print(f"Boss: {result.boss_slug}")
            print(f"  Rubric: {result.rubric_id}")
            print(f"  Score: {result.score} / {result.min_score_required}")
            print(f"  Grade: {result.grade}")
            print(f"  Passed: {'✓' if result.passed else '✗'}")
            print(f"  Boss HP: {result.boss_hp_before} → {result.boss_hp_after} (delta: {result.boss_hp_delta})")
            print(f"  Integrity: {result.integrity_before} → {result.integrity_after} (delta: {result.integrity_delta})")
            print()
        
        # Check overall pass
        if report.overall_pass:
            print("✅ All bosses passed QA!")
            return 0
        else:
            print("❌ One or more bosses failed QA")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(test_applylens_boss_qa())
