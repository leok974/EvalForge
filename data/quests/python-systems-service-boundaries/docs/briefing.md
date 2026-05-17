# Briefing: Service Boundaries & Contracts

## The Mission

Large systems are only as stable as their **boundaries**. When components talk to
each other through a shared interface, that interface must be explicit and reliable.

In this mission you will implement a small in-memory ticket store. A `Ticket` is a
frozen dataclass with an `id` (int) and a `status` (either `"open"` or `"closed"`).
`InMemoryTicketRepo` holds tickets in a dictionary and exposes two operations:
`get(ticket_id)` returns the ticket or `None`, and `save(ticket)` stores it.

The top-level function `close_ticket(repo, ticket_id)` loads a ticket by ID, sets
its status to `"closed"`, saves the updated ticket back to the repo, and returns
it. If the ticket does not exist, it must raise a `KeyError`.

This is a **pure core** implementation — no network calls, no global state, and no
`print` statements. The interface is the contract.
