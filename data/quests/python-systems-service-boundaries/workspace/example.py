from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Optional

# Example: a simple in-memory user store using the same repo pattern.
# Your task uses a Ticket repo; the pattern is identical.


@dataclass(frozen=True)
class User:
    id: int
    active: bool


class InMemoryUserRepo:
    def __init__(self):
        self._db: Dict[int, User] = {}

    def get(self, user_id: int) -> Optional[User]:
        return self._db.get(user_id)

    def save(self, user: User) -> None:
        self._db[user.id] = user


def deactivate_user(repo: InMemoryUserRepo, user_id: int) -> User:
    """Load user, set active=False, save, return. Raises KeyError if missing."""
    user = repo.get(user_id)
    if user is None:
        raise KeyError(f"user {user_id} not found")
    updated = replace(user, active=False)
    repo.save(updated)
    return updated
