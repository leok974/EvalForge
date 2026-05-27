# Hints: Service Boundaries & Contracts

## Hint 1 — Repository Boundary
Implement `InMemoryTicketRepo.get` and `save` first. They should be simple dictionary operations on `self._db`.

## Hint 2 — Service Logic
In `close_ticket`, use your repo's `get` method. If it returns `None`, you must raise a `KeyError` with the ticket ID to satisfy the contract.

## Hint 3 — Persistence

`Ticket` is a frozen dataclass — you cannot mutate it directly. Use `dataclasses.replace()` to create a new closed ticket, then save it:

```python
from dataclasses import replace

closed = replace(ticket, status="closed")
repo.save(closed)
return closed
```

Without calling `repo.save(closed)`, the change is not persisted to the "database" boundary.
