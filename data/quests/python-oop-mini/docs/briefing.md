# Briefing: Mini OOP System

## The Mission
The Reactor Core's internal ledger is currently a mess of global variables and scattered functions. We need to encapsulate the logic for handling account balances into a robust, reusable Class.

Your mission is to implement an `Account` class that can manage a balance, handle deposits, and safely process withdrawals.

## Objectives
- Create a class named `Account`.
- Implementation Details:
  - `__init__(self, balance=0)`: Initialize the account with an optional starting balance.
  - `deposit(self, amount)`: Increase the balance by the given amount.
  - `withdraw(self, amount)`: Decrease the balance by the given amount.
  - `balance` property: read the current balance via `account.balance`.
- Validation:
  - `deposit(amount)` must raise `ValueError` if `amount` is negative or zero.
  - `withdraw(amount)` must raise `ValueError` if `amount` is negative or zero.
  - `withdraw(amount)` must raise `ValueError` if `amount` exceeds the current balance (overdraft).
- All state must be stored within the instance (`self`).

## Constraints
- Do not use global variables.
- Follow Python naming conventions (CamelCase for classes).

## Example

```python
a = Account(100)
print(a.balance)   # 100

a.deposit(50)
print(a.balance)   # 150

a.withdraw(30)
print(a.balance)   # 120

a.deposit(-10)     # raises ValueError
a.withdraw(1000)   # raises ValueError (overdraft)
a.withdraw(-5)     # raises ValueError
```
