class Account:
    def __init__(self, balance: int = 0):
        self._balance = balance

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
        
    @property
    def balance(self):
        return self._balance
