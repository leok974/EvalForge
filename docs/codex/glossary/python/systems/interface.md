---
title: Interface (Abstract Base Class)
id: codex:glossary/python/systems/interface
world: python
---

# Interface

In Python, an **Interface** is a blueprint for a class. It defines a set of methods that implementing classes must define, but it does not implement them itself.

## Why use Interfaces?

- **Enforce Contracts:** Ensures that different classes adhere to the same structure.
- **Decoupling:** Code can rely on the interface rather than the specific implementation.
- **Testing:** Easier to mock dependencies.

## Python `abc` module

Python lacks a native `interface` keyword, so we use the `abc` (Abstract Base Classes) module:

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: int) -> bool:
        """Process a charge."""
        pass

class StripeGateway(PaymentGateway):
    def charge(self, amount: int) -> bool:
        print(f"Charging {amount} via Stripe")
        return True
```
