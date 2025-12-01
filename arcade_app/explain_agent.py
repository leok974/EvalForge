"""
ELARA: The Explain Agent with full codex integration.
"""
from __future__ import annotations

import json
import logging
from typing import AsyncGenerator, Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage

from arcade_app.persona_helper import get_npc
from arcade_app.database import get_session
from arcade_app.explain_helper import build_explain_system_prompt

logger = logging.getLogger(__name__)


async def load_codex_entry_by_id(codex_id: str) -> dict | None:
    """
    Load a codex entry from the database.
    
    Args:
        codex_id: Codex entry ID (e.g. "boss-reactor-core")
        
    Returns:
        Dict with title, summary, body_markdown or None if not found
    """
    from arcade_app.codex_helper import get_codex_entry
    
    # Try filesystem-based codex first
    entry = get_codex_entry(codex_id)
    if entry:
        return {
            "id": codex_id,
            "title": entry.get("metadata", {}).get("title", codex_id),
            "summary": entry.get("metadata", {}).get("summary", ""),
            "body_markdown": entry.get("content", ""),
        }
    
    return None


class ExplainAgent:
    """
    ELARA: Intelligent Teacher / Mentor agent.
    
    Context keys:
      - user_id (optional, for logging)
      - track_id (optional, for context)
      - codex_id (optional: which Codex entry to ground on)
      - hint_codex_id (alias for codex_id from Boss HUD)
    """

    name = "explain"

    async def run(
        self,
        user_input: str,
        context: Dict[str, Any],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream ELARA's explanation, optionally grounded in a specific Codex entry.
        
        Args:
            user_input: User's question
            context: Dict with user_id, track_id, codex_id, etc.
            
        Yields:
            SSE events: npc_identity, status, text_delta, done
        """
        user_id = context.get("user_id", "anonymous")
        track_id = context.get("track_id") or context.get("track")
        codex_id = (
            context.get("codex_id")
            or context.get("hint_codex_id")  # from Boss HUD
        )

        # 1) Identify ELARA to the frontend
        npc = get_npc("explain")
        yield {"event": "npc_identity", "data": json.dumps(npc)}

        # 2) Try to load Codex entry if provided
        codex_entry = None
        if codex_id:
            try:
                codex_entry = await load_codex_entry_by_id(codex_id)
                if codex_entry:
                    yield {
                        "event": "status",
                        "data": f"📚 Loading strategy guide: {codex_entry.get('title', codex_id)}"
                    }
                else:
                    logger.warning(
                        "Codex entry %s not found for user=%s", codex_id, user_id
                    )
            except Exception as exc:
                logger.exception(
                    "Failed to load codex entry %s for user=%s: %s",
                    codex_id,
                    user_id,
                    exc,
                )

        # 3) Build the system prompt (using tested helper)
        system_prompt = build_explain_system_prompt(
            user_input=user_input,
            track_id=track_id,
            codex_entry=codex_entry,
        )

        # 4) Get LLM and stream output
        try:
            from arcade_app.llm import get_chat_model
            
            llm = get_chat_model("explain")
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input),
            ]

            async for chunk in llm.astream(messages):
                # LangChain chunk has .content
                text = getattr(chunk, "content", None)
                if text:
                    yield {"event": "text_delta", "data": text}

        except Exception as exc:
            logger.exception("ExplainAgent LLM error for user=%s: %s", user_id, exc)
            yield {
                "event": "text_delta",
                "data": "⚠️ ELARA encountered an error while processing your request.",
            }

        yield {"event": "done", "data": "[DONE]"}
