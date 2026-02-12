import pytest

from workspace.task import Ticket, InMemoryTicketRepo, close_ticket


def test_close_ticket_happy_path():
  repo = InMemoryTicketRepo({1: Ticket(id=1, status="open")})
  updated = close_ticket(repo, 1)

  assert updated.status == "closed"
  assert repo.get(1).status == "closed"


def test_close_ticket_missing_raises_keyerror():
  repo = InMemoryTicketRepo({})
  with pytest.raises(KeyError):
    close_ticket(repo, 999)
