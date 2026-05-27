# Tutorial: Service Boundaries

A service boundary is where your application logic meets external data or storage. At this point, the system must enforce strict **Contracts**.

## Repository Pattern
A **Repository** abstracts away data storage. It provides a clean boundary so your business logic doesn't care if the data is in a dictionary, a file, or a database.

```python
class InMemoryRepo:
    def __init__(self, initial=None):
        self._db = initial or {}

    def get(self, id):
        return self._db.get(id)

    def save(self, obj):
        self._db[obj.id] = obj
```

## Boundary Logic
In this quest, your **Service** logic (`close_ticket`) must interact with the **Repository** boundary:

1.  **Retrieve**: Load the domain object (the `Ticket`) from the boundary.
2.  **Validate**: Ensure the object exists. If not, raise an error (e.g., `KeyError`).
3.  **Update**: Apply the business logic (set status to `"closed"`).
4.  **Persist**: Save the updated object back to the boundary.

## Frozen Dataclasses & `dataclasses.replace()`

`Ticket` is defined with `@dataclass(frozen=True)`. Frozen dataclasses are **immutable** — direct attribute assignment raises a `FrozenInstanceError`:

```python
ticket.status = "closed"  # FrozenInstanceError: cannot assign to field 'status'
```

Use `dataclasses.replace()` to create a new instance with the updated field:

```python
from dataclasses import replace

ticket = repo.get(101)
closed = replace(ticket, status="closed")
repo.save(closed)
```

`replace()` copies all fields from `ticket` and overrides only the ones you specify. The original `ticket` object is unchanged; `closed` is the new immutable instance you save.

By separating storage (Repository) from logic (Service), your code remains testable and scalable.
