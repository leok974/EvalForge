"""
QA Run Limiter - Prevent DoS via concurrent execution limits.

Limits:
- Global: 5 concurrent runs across all users
- Per-user: 3 concurrent runs per user

Usage:
    from arcade_app.services.qa_limits import qa_limiter
    
    if not await qa_limiter.can_start_run(user_id):
        raise HTTPException(status_code=429, detail="Too many concurrent runs")
    
    await qa_limiter.register_run(run_id, user_id)
    # ... execute run ...
    await qa_limiter.unregister_run(run_id)
"""
import os
import asyncio
from typing import Dict

class QARunLimiter:
    """Thread-safe concurrent run limiter for QA operations."""
    
    def __init__(self):
        # Configurable limits via env vars
        self.global_limit = int(os.getenv("QA_GLOBAL_RUN_LIMIT", "5"))
        self.per_user_limit = int(os.getenv("QA_PER_USER_LIMIT", "3"))
        
        # Track active runs: {run_id: user_id}
        self.active_runs: Dict[str, str] = {}
        
        # Thread-safe lock for concurrent access
        self.lock = asyncio.Lock()
    
    async def can_start_run(self, user_id: str) -> bool:
        """
        Check if user can start a new run.
        
        Returns:
            True if within limits, False otherwise
        """
        async with self.lock:
            # Check global limit
            if len(self.active_runs) >= self.global_limit:
                return False
            
            # Check per-user limit
            user_run_count = sum(1 for uid in self.active_runs.values() if uid == user_id)
            if user_run_count >= self.per_user_limit:
                return False
            
            return True
    
    async def register_run(self, run_id: str, user_id: str):
        """
        Register a new active run.
        
        Args:
            run_id: Unique run identifier
            user_id: User who triggered the run
        """
        async with self.lock:
            self.active_runs[run_id] = user_id
    
    async def unregister_run(self, run_id: str):
        """
        Remove completed/failed run from tracking.
        
        Args:
            run_id: Run identifier to remove
        """
        async with self.lock:
            self.active_runs.pop(run_id, None)
    
    async def get_active_count(self, user_id: str | None = None) -> int:
        """
        Get count of active runs (optionally filtered by user).
        
        Args:
            user_id: If provided, count only this user's runs
        
        Returns:
            Count of active runs
        """
        async with self.lock:
            if user_id:
                return sum(1 for uid in self.active_runs.values() if uid == user_id)
            return len(self.active_runs)


# Global singleton instance
qa_limiter = QARunLimiter()
