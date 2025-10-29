"""
In-memory session state management for EvalForge.
Tracks onboarding progress and user preferences per session.
"""
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
import hashlib


class Grade(BaseModel):
    """Pydantic model for Judge grading rubric."""
    coverage: int = Field(ge=0, le=5)
    correctness: int = Field(ge=0, le=5)
    clarity: int = Field(ge=0, le=5)
    comment: str = Field(max_length=280, default="Good start—see notes.")
    rubric: tuple[str, str, str] = ("coverage", "correctness", "clarity")
    version: int = Field(ge=1, default=1)


def normalize_for_hash(s: str) -> str:
    """
    Trim, collapse trailing spaces per-line, preserve newlines.
    This makes hashes stable across trivial edits.
    """
    s = s.strip()
    return "\n".join(line.rstrip() for line in s.splitlines())


def sha1_of_text(s: str) -> str:
    """Compute SHA1 hash of text for deduplication."""
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


@dataclass
class SessionState:
    """State tracked per session for personalized onboarding."""
    greeted: bool = False
    judge_intro_done: bool = False
    track: Optional[str] = None  # "debugging", "cloud", or "llm"
    blurb: str = field(default="EvalForge: an AI Trainer Arcade that evaluates your answers, coaches you like a mentor, and builds you a personalized training path around real engineering skills.")
    # Cloud track troubleshooting memory
    issue_summary: Optional[str] = None  # Current issue being debugged (for cloud track)
    next_step: Optional[str] = None  # Recommended next action (for cloud track)
    # Debugging track code review memory
    debug_problem: Optional[str] = None  # Short label of what's wrong in their code
    debug_next_step: Optional[str] = None  # What they should try next / how to fix it
    language_hint: Optional[str] = None  # "python", "javascript", etc. if we can infer
    # Grading / scoreboard memory (Phase 3)
    last_grade: Optional[Grade] = None  # Most recent rubric evaluation (coverage, correctness, clarity, comment)
    last_graded_input_hash: Optional[str] = None  # Hash of last graded submission (prevents re-grading)


class SessionStore:
    """In-memory store for session states."""
    
    def __init__(self):
        self._store: Dict[str, SessionState] = {}
    
    def get(self, session_id: str) -> SessionState:
        """Get or create session state for a session ID."""
        if session_id not in self._store:
            self._store[session_id] = SessionState()
        return self._store[session_id]
    
    def update(self, session_id: str, **kwargs: Any) -> SessionState:
        """Update specific fields in session state."""
        state = self.get(session_id)
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        return state
    
    def clear(self, session_id: str) -> None:
        """Clear session state (for testing/reset)."""
        if session_id in self._store:
            del self._store[session_id]
    
    def get_state_dict(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session state as a dictionary for debugging/introspection."""
        if session_id not in self._store:
            return None
        state = self.get(session_id)
        return {
            "greeted": state.greeted,
            "judge_intro_done": state.judge_intro_done,
            "track": state.track,
            "blurb": state.blurb,
            "issue_summary": state.issue_summary,
            "next_step": state.next_step,
            "debug_problem": state.debug_problem,
            "debug_next_step": state.debug_next_step,
            "language_hint": state.language_hint,
            "last_grade": state.last_grade,
            "last_graded_input_hash": state.last_graded_input_hash,
        }


# Global session store instance
session_store = SessionStore()
