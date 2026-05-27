import pytest
from main import InMemoryTicketRepo, Ticket, close_ticket


def test_close_open_ticket():
    repo = InMemoryTicketRepo({1: Ticket(id=1, status="open")})
    closed = close_ticket(repo, 1)
    assert closed.status == "closed"
    assert closed.id == 1


def test_closed_ticket_persisted():
    repo = InMemoryTicketRepo({1: Ticket(id=1, status="open")})
    close_ticket(repo, 1)
    assert repo.get(1).status == "closed"


def test_missing_ticket_raises_key_error():
    repo = InMemoryTicketRepo()
    with pytest.raises(KeyError):
        close_ticket(repo, 99)


def test_repo_get_returns_none_for_missing():
    repo = InMemoryTicketRepo()
    assert repo.get(42) is None


def test_repo_save_and_get():
    repo = InMemoryTicketRepo()
    ticket = Ticket(id=7, status="open")
    repo.save(ticket)
    assert repo.get(7) == ticket
