from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Ticket:
    id: int
    status: str  # "open" or "closed"


class InMemoryTicketRepo:
    def __init__(self, initial: Optional[Dict[int, Ticket]] = None):
        self._db: Dict[int, Ticket] = dict(initial or {})

    def get(self, ticket_id: int) -> Optional[Ticket]:
        # TODO: return the Ticket with the given id, or None if not found
        raise NotImplementedError("TODO: implement get(ticket_id)")

    def save(self, ticket: Ticket) -> None:
        # TODO: store ticket in self._db keyed by ticket.id
        raise NotImplementedError("TODO: implement save(ticket)")


def close_ticket(repo: InMemoryTicketRepo, ticket_id: int) -> Ticket:
    # TODO: load the ticket (raise KeyError if not found)
    # TODO: create a new Ticket with status="closed" and save it
    # TODO: return the closed ticket
    raise NotImplementedError("TODO: implement close_ticket(repo, ticket_id)")
