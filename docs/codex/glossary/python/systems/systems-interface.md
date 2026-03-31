---
id: glossary/python/systems/interface
title: Interface
world: python
level: intermediate
tags: [architecture, abstraction, duck-typing]
related:
  - codex:glossary/python/systems/dependency-injection
  - codex:glossary/python/systems/separation-of-concerns
  - codex:glossary/python/dictionary
---

## Definition
An **interface** defines a contract for what methods a class should implement, without specifying how. In Python, interfaces are typically defined using abstract base classes (ABC) or duck typing ("if it walks like a duck...").

## Usage
- Define interfaces with `abc.ABC` and `@abstractmethod`.
- Code against interfaces, not concrete implementations.
- Swap implementations without changing client code.

## Example
```python
from abc import ABC, abstractmethod

# Define interface
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Implementations
class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via Stripe")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via PayPal")

# Client code works with any PaymentProcessor
def checkout(processor: PaymentProcessor, amount):
    processor.process_payment(amount)
```

## Pitfalls

* Over-using interfaces for simple code adds boilerplate.
* Python's duck typing often makes explicit interfaces unnecessary.

## Related

* Dependency Injection: DI works best with interfaces.
* Separation of Concerns: interfaces help separate concerns.
* Dictionary: dicts can act as simple interfaces (duck typing).