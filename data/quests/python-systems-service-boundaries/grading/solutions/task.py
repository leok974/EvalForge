from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Ticket:
  id: int
  status: str


class InMemoryTicketRepo:
  def __init__(self, initial: Optional[Dict[int, Ticket]] = None):
    self._db: Dict[int, Ticket] = dict(initial or {})

  def get(self, ticket_id: int) -> Optional[Ticket]:
    return self._db.get(ticket_id)

  def save(self, ticket: Ticket) -> None:
    self._db[ticket.id] = ticket


def close_ticket(repo: InMemoryTicketRepo, ticket_id: int) -> Ticket:
  existing = repo.get(ticket_id)
  if existing is None:
    raise KeyError(ticket_id)
  updated = Ticket(id=existing.id, status="closed")
  repo.save(updated)
  return updated
