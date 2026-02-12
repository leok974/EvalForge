"""
Quest: python-systems-service-boundaries

Implement clean service/repo boundaries using an in-memory repository.

Implement:
- Ticket dataclass: id:int, status:str ("open" or "closed")
- InMemoryTicketRepo with:
    - get(ticket_id) -> Ticket | None
    - save(ticket) -> None
- close_ticket(repo, ticket_id) -> Ticket
    - load ticket, set status to "closed", save, return
    - raise KeyError if not found
"""

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
    raise NotImplementedError("TODO: implement get(ticket_id)")

  def save(self, ticket: Ticket) -> None:
    raise NotImplementedError("TODO: implement save(ticket)")


def close_ticket(repo: InMemoryTicketRepo, ticket_id: int) -> Ticket:
  raise NotImplementedError("TODO: implement close_ticket(repo, ticket_id)")
