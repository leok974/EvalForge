"""
Tests for explain helper with codex integration.
"""
from arcade_app.explain_helper import build_explain_system_prompt


def test_build_explain_system_prompt_without_codex():
    """Without codex, should use general explain prompt."""
    prompt = build_explain_system_prompt(
        user_input="Why did I fail the boss?",
        track_id="world-python",
        codex_entry=None,
    )
    assert "Why did I fail the boss?" in prompt
    assert "CODEX CONTEXT" not in prompt
    assert "ELARA" in prompt or "Archivist" in prompt


def test_build_explain_system_prompt_with_codex_includes_content():
    """With codex, should include title, summary, and body in prompt."""
    codex = {
        "id": "boss-reactor-core",
        "title": "Boss: Reactor Core",
        "summary": "Explains the timed boss mechanics and HP drain.",
        "body_markdown": "## Key Mechanic\nOn second failure, unlocks strategy guide.\n\n## Tips\n- Read error messages carefully",
    }

    prompt = build_explain_system_prompt(
        user_input="How do I beat Reactor Core?",
        track_id="world-evalforge",
        codex_entry=codex,
    )

    # Verify codex content is in prompt
    assert "Boss: Reactor Core" in prompt
    assert "boss-reactor-core" in prompt
    assert "On second failure, unlocks strategy guide." in prompt
    assert "How do I beat Reactor Core?" in prompt
    assert "CODEX CONTEXT" in prompt
    assert "ELARA" in prompt or "Archivist" in prompt


def test_build_explain_system_prompt_codex_trumps_general_rag():
    """With codex, prompt should emphasize using that doc as authoritative."""
    codex = {
        "id": "boss-reactor-core",
        "title": "Reactor Core Strategy",
        "summary": "Official strategy guide",
        "body_markdown": "Step 1: Check your code\nStep 2: Run tests",
    }

    prompt = build_explain_system_prompt(
        user_input="Help me debug this",
        track_id=None,
        codex_entry=codex,
    )

    # Should instruct to use codex as primary reference
    assert "authoritative" in prompt.lower() or "primary" in prompt.lower()
    assert "Step 1: Check your code" in prompt
    assert "Step 2: Run tests" in prompt
