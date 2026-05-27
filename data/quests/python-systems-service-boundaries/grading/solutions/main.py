from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Dict, Optional


@dataclass(frozen=True)
class Ticket:
    id: int
    status: str  # "open" or "closed"


class InMemoryTicketRepo:
    def __init__(self, initial: Optional[Dict[int, "Ticket"]] = None):
        self._db: Dict[int, "Ticket"] = dict(initial or {})

    def get(self, ticket_id: int) -> Optional["Ticket"]:
        return self._db.get(ticket_id)

    def save(self, ticket: "Ticket") -> None:
        self._db[ticket.id] = ticket


def close_ticket(repo: InMemoryTicketRepo, ticket_id: int) -> Ticket:
    ticket = repo.get(ticket_id)
    if ticket is None:
        raise KeyError(f"ticket {ticket_id} not found")
    closed = replace(ticket, status="closed")
    repo.save(closed)
    return closed
