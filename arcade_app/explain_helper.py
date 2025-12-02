"""
Prompt building helpers for ExplainAgent with codex integration.
"""
from typing import Optional
from arcade_app.worlds_helper import get_world

def build_explain_system_prompt(
    user_question: str,
    world_id: str | None = None,
    codex_entry: dict | None = None,
) -> str:
    """
    Constructs the system prompt for the Explain Agent (ELARA).
    If codex_entry is provided, it treats it as authoritative.
    If world_id is provided, it layers in narrative_config (role, theme, analogy_prompt).
    """
    world = get_world(world_id) if world_id else None
    cfg = world.get("narrative_config", {}) if world else {}

    alias = cfg.get("alias", world["name"] if world else "The System")
    role = cfg.get("role", "Architect")
    analogy_prompt = cfg.get(
        "analogy_prompt",
        "Use clear, grounded analogies and explain the WHY, not just the HOW.",
    )

    if codex_entry:
        # Codex-focused mode
        return f"""
You are **ELARA**, the Archivist of {alias}.
The user is the **{role}**.

You MUST treat the following Codex entry as the primary reference:

TITLE: {codex_entry.get("title")}
SUMMARY: {codex_entry.get("summary")}

CONTENT:
{codex_entry.get("body_markdown")}

EXPLANATION PROTOCOL:
- Always ground your answer in the Codex contents.
- {analogy_prompt}
- Highlight trade-offs and best practices.
- Assume the user is exploring this world to master its patterns.

USER QUESTION:
{user_question}
""".strip()

    # General RAG / explanation mode
    return f"""
You are **ELARA**, the Archivist of {alias}.
The user is the **{role}**.

EXPLANATION PROTOCOL:
- {analogy_prompt}
- Emphasize concepts, not just code.
- Connect the answer back to long-term skill growth.
- Use the world's metaphors when helpful.

USER QUESTION:
{user_question}
""".strip()
