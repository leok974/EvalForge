# Hints: Mini OOP System

## Hint 1 — Concept
Start by defining the `Account` class and the `__init__` method. Store the value in `self._balance`. Then add a `balance` property so the test can read it via `account.balance`:

```python
@property
def balance(self):
    return self._balance
```

## Hint 2 — Guided
In `deposit`, validate before modifying state. Reject non-positive amounts and raise `ValueError`:

```python
def deposit(self, amount: int):
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    self._balance += amount
```

Apply the same pattern to `withdraw` — also check that `amount` does not exceed `self._balance` (overdraft guard).

## Hint 3 — The Solution
The test suite creates an instance and calls methods. Ensure method names, the `balance` property, and all `ValueError` guards match exactly:

```python
class Account:
    def __init__(self, balance: int = 0):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```
