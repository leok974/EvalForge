import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from arcade_app.bosses.boss_progress_helper import update_boss_progress
from arcade_app.models import BossProgress
from arcade_app.explain_agent import load_codex_entry_by_id
from arcade_app.explain_helper import build_explain_system_prompt

@pytest.mark.asyncio
async def test_boss_failure_unlocks_hint(monkeypatch):
    """
    Integration test for the 'Happy Path of Failure':
    1. User fails boss twice.
    2. Hint unlocks.
    3. ELARA uses the hint in her prompt.
    """
    
    # --- 1. Setup Mock Database Session ---
    mock_session = AsyncMock()
    
    # Mock execute result for select(BossProgress)
    # First call: returns None (new record)
    # Subsequent calls: returns the record we "added"
    
    stored_progress = None
    
    async def fake_execute(stmt):
        nonlocal stored_progress
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = stored_progress
        return mock_result
        
    mock_session.execute = fake_execute
    
    def fake_add(instance):
        nonlocal stored_progress
        stored_progress = instance
        
    mock_session.add = fake_add
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    user_id = "test_user_fail_loop"
    boss_id = "boss-reactor-core"
    
    # --- 2. Simulate Failure 1 ---
    result1 = await update_boss_progress(mock_session, user_id, boss_id, "fail")
    
    assert result1["fail_streak"] == 1
    assert result1["hint_unlocked"] is False
    assert stored_progress.fail_streak == 1
    
    # --- 3. Simulate Failure 2 (Threshold) ---
    result2 = await update_boss_progress(mock_session, user_id, boss_id, "fail")
    
    assert result2["fail_streak"] == 2
    assert result2["hint_unlocked"] is True
    assert result2["hint_codex_id"] == "boss-reactor-core"
    assert stored_progress.highest_hint_level == 1
    
    # --- 4. Verify Codex Loading ---
    # This relies on the file we created in Step 1
    codex_id = result2["hint_codex_id"]
    entry = await load_codex_entry_by_id(codex_id)
    
    assert entry is not None
    assert entry["id"] == "boss-reactor-core"
    assert "Strategy Guide" in entry["title"]
    assert "Winning Strategy" in entry["body_markdown"]
    
    # --- 5. Verify ELARA Prompt Construction ---
    # Now we simulate the user clicking "Ask ELARA" with this codex_id
    
    prompt = build_explain_system_prompt(
        user_input="How do I beat this?",
        track_id="world-evalforge",
        codex_entry=entry
    )
    
    print(f"Generated Prompt:\n{prompt}")
    
    # Assertions on the prompt
    assert "CODEX CONTEXT" in prompt
    assert "Strategy Guide: The Reactor Core" in prompt
    assert "Winning Strategy" in prompt
    assert "Async Concurrency" in prompt # From the markdown content
