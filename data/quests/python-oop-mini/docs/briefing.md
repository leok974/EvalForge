# Briefing: Mini OOP System

## The Mission
The Reactor Core's internal ledger is currenty a mess of global variables and scattered functions. We need to encapsulate the logic for handling account balances into a robust, reusable Class.

Your mission is to implement an `Account` class that can manage a balance, handle deposits, and safely process withdrawals.

## Objectives
- Create a class named `Account`.
- Implementation Details:
  - `__init__(self, balance=0)`: Initialize the account with an optional starting balance.
  - `deposit(self, amount)`: Increase the balance by the given amount.
  - `withdraw(self, amount)`: Decrease the balance by the given amount.
- Validation:
  - Ensure that withdrawals do not exceed the current balance (optional, but good practice).
  - Methods should update the instance's state correctly.

## Constraints
- Do not use global variables. All state must be stored within the instance (`self`).
- Follow Python naming conventions (CamelCase for classes).
