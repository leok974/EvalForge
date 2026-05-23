# Hints: Service Boundaries & Contracts

## Hint 1 — Repository Boundary
Implement `InMemoryTicketRepo.get` and `save` first. They should be simple dictionary operations on `self._db`.

## Hint 2 — Service Logic
In `close_ticket`, use your repo's `get` method. If it returns `None`, you must raise a `KeyError` with the ticket ID to satisfy the contract.

## Hint 3 — Persistence
Don't forget to call `repo.save(ticket)` after you update the status. Without this step, your changes stay in memory but aren't persisted to the "database" boundary.
