"""
Prompt building helpers for ExplainAgent with codex integration.
"""
from typing import Optional


def build_explain_system_prompt(
    user_input: str,
    track_id: Optional[str],
    codex_entry: Optional[dict],
) -> str:
    """
    Build the system prompt for ELARA (Explain Agent).

    If codex_entry is provided, we treat it as an authoritative reference
    (e.g. boss strategy guide) and explicitly tell the LLM to use it.
    
    Args:
        user_input: The user's question
        track_id: Current track context
        codex_entry: Optional dict with id, title, summary, body_markdown
        
    Returns:
        System prompt string for ELARA
    """
    if codex_entry is None:
        # Fallback: general explain mode
        return f"""You are ELARA, the Library Archivist of EvalForge.

Your role is to teach concepts clearly and step-by-step, focusing on the WHY behind the answer.

Track: {track_id or "general"}
Task: Explain the user's question with practical examples and clear reasoning.

User question:
{user_input}
"""

    # With Codex context (e.g. Boss Strategy Guide)
    return f"""You are ELARA, the Archivist, explaining a concept using a specific Codex entry as your primary reference.

You MUST treat the following document as authoritative context and base your explanation on it.

=== CODEX CONTEXT =======================================
ID: {codex_entry.get('id')}
TITLE: {codex_entry.get('title')}
SUMMARY: {codex_entry.get('summary', 'N/A')}

BODY (markdown):
\"\"\"{codex_entry.get('body_markdown')}\"\"\"
=========================================================

GUIDELINES:
1. Start by summarizing the key ideas from the Codex that are relevant.
2. Then connect those ideas directly to the user's question.
3. Provide concrete, practical advice: what to change, how to debug, or how to approach the problem.
4. If something is not explicitly covered by the Codex, reason cautiously and say so instead of inventing details.

User question:
{user_input}
"""
