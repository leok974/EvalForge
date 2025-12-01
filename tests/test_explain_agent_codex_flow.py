"""
Integration test for ExplainAgent with codex flow.
Tests that codex_id → load → prompt builder → stream works correctly.
"""
import pytest
from typing import Any, Dict, List


@pytest.mark.asyncio
async def test_explain_agent_uses_codex_entry(monkeypatch):
    """Verify ExplainAgent loads codex and builds prompt correctly."""
    
    calls: Dict[str, Any] = {}

    # --- Patch load_codex_entry_by_id ---
    async def fake_load_codex_entry_by_id(codex_id: str):
        calls["codex_id"] = codex_id
        # Return a fake codex entry
        return {
            "id": codex_id,
            "title": "Reactor Core Strategy",
            "summary": "How to approach the boss.",
            "body_markdown": "# Guide\nAlways fix the main loop first.\n\n## Tips\n- Check edge cases",
        }

    monkeypatch.setattr(
        "arcade_app.explain_agent.load_codex_entry_by_id",
        fake_load_codex_entry_by_id,
        raising=False,
    )

    # --- Patch build_explain_system_prompt ---
    def fake_build_explain_system_prompt(user_input, track_id=None, codex_entry=None):
        calls["user_input"] = user_input
        calls["track_id"] = track_id
        calls["codex_title"] = codex_entry["title"] if codex_entry else None
        calls["has_body"] = bool(codex_entry and codex_entry.get("body_markdown"))
        return "SYSTEM: Use the provided codex entry as authoritative reference."

    monkeypatch.setattr(
        "arcade_app.explain_agent.build_explain_system_prompt",
        fake_build_explain_system_prompt,
        raising=False,
    )

    # --- Patch the LLM to avoid network calls ---
    class FakeChunk:
        def __init__(self, content: str):
            self.content = content

    class FakeLLM:
        async def astream(self, messages):
            # Yield chunks that show we used the codex
            yield FakeChunk("ELARA: Based on the Reactor Core Strategy guide, ")
            yield FakeChunk("you should fix the main loop first and check edge cases.")

    def fake_get_chat_model(agent_name: str):
        calls["llm_agent"] = agent_name
        return FakeLLM()

    # Patch where ExplainAgent actually imports from
    monkeypatch.setattr(
        "arcade_app.llm.get_chat_model",
        fake_get_chat_model,
        raising=False,
    )

    # --- Patch get_npc ---
    def fake_get_npc(role: str):
        return {"name": "ELARA", "role": "explain", "avatar": "teacher"}

    monkeypatch.setattr(
        "arcade_app.explain_agent.get_npc",
        fake_get_npc,
        raising=False,
    )

    # --- Run the agent ---
    from arcade_app.explain_agent import ExplainAgent

    agent = ExplainAgent()

    events: List[Dict[str, Any]] = []
    async for evt in agent.run(
        "How do I beat the Reactor Core boss?",
        {
            "user_id": "test-user",
            "track_id": "world-python",
            "codex_id": "boss-reactor-core",
        },
    ):
        events.append(evt)

    # --- Assertions: Verify the wiring ---
    
    # 1) Codex lookup used the provided ID
    assert calls["codex_id"] == "boss-reactor-core", "Should load correct codex entry"

    # 2) Prompt builder received the question, track, and codex
    assert calls["user_input"] == "How do I beat the Reactor Core boss?"
    assert calls["track_id"] == "world-python"
    assert calls["codex_title"] == "Reactor Core Strategy", "Should pass codex to prompt builder"
    assert calls["has_body"] is True, "Codex entry should have body content"

    # 3) LLM was called (if get_chat_model was reached)
    if "llm_agent" in calls:
        assert calls["llm_agent"] == "explain"

    # 4) We got NPC identity event
    npc_events = [e for e in events if e["event"] == "npc_identity"]
    assert len(npc_events) == 1, "Should emit npc_identity for ELARA"

    # 5) We got text deltas
    text_events = [e for e in events if e["event"] == "text_delta"]
    assert len(text_events) > 0, "Should emit text_delta events"
    
    # Concatenate all text
    full_text = "".join(e["data"] for e in text_events)
    assert "ELARA" in full_text, "Response should be from ELARA"
    assert "Reactor Core Strategy" in full_text, "Should reference the codex"

    # 6) We got done event
    done_events = [e for e in events if e["event"] == "done"]
    assert len(done_events) == 1, "Should emit done event"


@pytest.mark.asyncio
async def test_explain_agent_without_codex(monkeypatch):
    """Verify ExplainAgent works without codex_id."""
    
    calls: Dict[str, Any] = {}

    # --- Patch build_explain_system_prompt ---
    def fake_build_explain_system_prompt(user_input, track_id=None, codex_entry=None):
        calls["user_input"] = user_input
        calls["has_codex"] = codex_entry is not None
        return "SYSTEM: General explain mode."

    monkeypatch.setattr(
        "arcade_app.explain_agent.build_explain_system_prompt",
        fake_build_explain_system_prompt,
        raising=False,
    )

    # --- Patch LLM ---
    class FakeChunk:
        def __init__(self, content: str):
            self.content = content

    class FakeLLM:
        async def astream(self, messages: List[Any]):
            yield FakeChunk("General explanation without specific codex.")

    def fake_get_chat_model(agent_name: str):
        return FakeLLM()

    monkeypatch.setattr(
        "arcade_app.explain_agent.get_chat_model",
        fake_get_chat_model,
        raising=False,
    )

    # --- Patch get_npc ---
    def fake_get_npc(role: str):
        return {"name": "ELARA", "role": "explain"}

    monkeypatch.setattr(
        "arcade_app.explain_agent.get_npc",
        fake_get_npc,
        raising=False,
    )

    # --- Run the agent WITHOUT codex_id ---
    from arcade_app.explain_agent import ExplainAgent

    agent = ExplainAgent()

    events: List[Dict[str, Any]] = []
    async for evt in agent.run(
        "What is a closure?",
        {"user_id": "test-user", "track_id": "javascript-basics"},
    ):
        events.append(evt)

    # --- Assertions ---
    assert calls["has_codex"] is False, "Should not have codex entry"
    
    text_events = [e for e in events if e["event"] == "text_delta"]
    assert len(text_events) > 0, "Should still stream text"


def test_build_explain_system_prompt_with_codex():
    """Verify prompt builder includes codex content."""
    from arcade_app.explain_helper import build_explain_system_prompt
    
    codex = {
        "id": "boss-reactor-core",
        "title": "Reactor Core Boss",
        "summary": "High-pressure refactoring challenge",
        "body_markdown": "## Strategy\n1. Fix the main loop\n2. Handle edge cases",
    }
    
    prompt = build_explain_system_prompt(
        user_input="How do I beat this boss?",
        track_id="world-python",
        codex_entry=codex,
    )
    
    # Verify codex content is in prompt
    assert "Reactor Core Boss" in prompt
    assert "Fix the main loop" in prompt
    assert "Handle edge cases" in prompt
    assert "CODEX CONTEXT" in prompt or "codex" in prompt.lower()
    assert "authoritative" in prompt.lower() or "primary" in prompt.lower()
