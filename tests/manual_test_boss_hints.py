"""
Manual E2E test script for boss strategy guide system.

This script simulates the full boss hint unlock flow:
1. Create test user
2. Fail boss twice
3. Verify hint unlocks
4. Verify win resets streak
"""
import asyncio
from arcade_app.database import init_db, get_session
from arcade_app.models import BossProgress
from arcade_app.bosses.boss_progress_helper import update_boss_progress
from sqlmodel import select


async def test_boss_hint_flow():
    """Test the complete boss hint unlock flow."""
    print("🎮 Boss Strategy Guide E2E Test\n")
    print("=" * 50)
    
    # Initialize DB
    print("\n1. Initializing database...")
    await init_db()
    print("✅ Database initialized")
    
    async for session in get_session():
        # Clean up any existing progress
        print("\n2. Cleaning up test data...")
        stmt = select(BossProgress).where(
            BossProgress.user_id == "test_user_e2e",
            BossProgress.boss_id == "boss-reactor-core"
        )
        result = await session.exec(stmt)
        existing = result.first()
        if existing:
            await session.delete(existing)
            await session.commit()
        print("✅ Test data cleaned")
        
        # Test 1: First failure (no hint)
        print("\n3. Testing first failure (no hint expected)...")
        result1 = await update_boss_progress(
            session,
            user_id="test_user_e2e",
            boss_id="boss-reactor-core",
            outcome="fail"
        )
        print(f"   Fail streak: {result1['fail_streak']}")
        print(f"   Hint codex ID: {result1['hint_codex_id']}")
        assert result1["fail_streak"] == 1, "Expected fail_streak=1"
        assert result1["hint_codex_id"] is None, "Expected no hint"
        print("✅ First failure: No hint unlocked (correct)")
        
        # Test 2: Second failure (hint unlocks!)
        print("\n4. Testing second consecutive failure (hint should unlock)...")
        result2 = await update_boss_progress(
            session,
            user_id="test_user_e2e",
            boss_id="boss-reactor-core",
            outcome="fail"
        )
        print(f"   Fail streak: {result2['fail_streak']}")
        print(f"   Hint codex ID: {result2['hint_codex_id']}")
        assert result2["fail_streak"] == 2, "Expected fail_streak=2"
        assert result2["hint_codex_id"] == "boss-reactor-core", "Expected hint to unlock"
        print("✅ Second failure: Strategy Guide unlocked! 📚")
        
        # Test 3: Win resets streak
        print("\n5. Testing win (should reset streak)...")
        result3 = await update_boss_progress(
            session,
            user_id="test_user_e2e",
            boss_id="boss-reactor-core",
            outcome="win"
        )
        print(f"   Fail streak: {result3['fail_streak']}")
        print(f"   Hint codex ID: {result3['hint_codex_id']}")
        assert result3["fail_streak"] == 0, "Expected fail_streak=0 after win"
        assert result3["hint_codex_id"] is None, "Expected no hint after win"
        print("✅ Win: Streak reset to 0 (correct)")
        
        # Test 4: Verify persistence
        print("\n6. Verifying database persistence...")
        stmt = select(BossProgress).where(
            BossProgress.user_id == "test_user_e2e",
            BossProgress.boss_id == "boss-reactor-core"
        )
        result = await session.exec(stmt)
        progress = result.first()
        assert progress is not None, "Progress should exist in DB"
        assert progress.fail_streak == 0, "DB should show fail_streak=0"
        assert progress.last_outcome == "win", "DB should show last_outcome=win"
        print("✅ Database persistence verified")
        
        # Cleanup
        print("\n7. Cleaning up...")
        await session.delete(progress)
        await session.commit()
        print("✅ Cleanup complete")
        
        break
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("\n📋 Summary:")
    print("  ✅ Fail streak increments correctly")
    print("  ✅ Hint unlocks after 2 consecutive failures")
    print("  ✅ Win resets fail streak to 0")
    print("  ✅ Data persists to database correctly")
    print("\n🚀 Boss Strategy Guide system is ready for production!")


if __name__ == "__main__":
    asyncio.run(test_boss_hint_flow())
