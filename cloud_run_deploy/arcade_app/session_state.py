"""
In-memory session state management for EvalForge.
Tracks onboarding progress and user preferences per session.
"""
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class SessionState:
    """State tracked per session for personalized onboarding."""
    greeted: bool = False
    judge_intro_done: bool = False
    track: Optional[str] = None  # "debugging", "cloud", or "llm"
    blurb: str = field(default="EvalForge: an AI Trainer Arcade that evaluates your answers, coaches you like a mentor, and builds you a personalized training path around real engineering skills.")


class SessionStore:
    """In-memory store for session states."""
    
    def __init__(self):
        self._store: Dict[str, SessionState] = {}
    
    def get(self, session_id: str) -> SessionState:
        """Get or create session state for a session ID."""
        if session_id not in self._store:
            self._store[session_id] = SessionState()
        return self._store[session_id]
    
    def update(self, session_id: str, **kwargs) -> SessionState:
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
    
    def get_state_dict(self, session_id: str) -> dict:
        """Get session state as a dictionary for debugging/introspection."""
        state = self.get(session_id)
        return {
            "greeted": state.greeted,
            "judge_intro_done": state.judge_intro_done,
            "track": state.track,
            "blurb": state.blurb,
        }


# Global session store instance
session_store = SessionStore()
