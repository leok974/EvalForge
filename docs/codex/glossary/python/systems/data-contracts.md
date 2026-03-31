---
id: glossary/python/systems/data-contracts
title: Data Contracts
world: python
level: intermediate
tags: [architecture, design, api]
related:
  - codex:glossary/python/systems/interface
  - codex:glossary/python/typing
---

## Definition
A **data contract** is a formal agreement between two parts of a system (or different systems) about the structure, format, and meaning of the data they exchange. It ensures that consumers can depend on a stable data shape.

## Usage
- Define contracts using type hints (`TypedDict`, `dataclasses`, `Pydantic`).
- Validate incoming data at the boundaries (gateways, API handlers).
- Ensure that changes to the internal implementation do not break the external contract.

## Example
```python
from typing import TypedDict

class UserContract(TypedDict):
    id: int
    name: str
    email: str | None

def process_user(data: UserContract):
    # The function can safely assume 'id' and 'name' are present and typed correctly
    print(f"Processing {data['name']} (ID: {data['id']})")
```

## Pitfalls
- Implicit contracts (using generic `dict`) make it hard to know what fields are required.
- Breaking a contract without versioning causes system-wide failures.

## Related
- Interface: Contracts are often implemented via interfaces.
- Typing: Python's typing system is the primary tool for defining contracts.
