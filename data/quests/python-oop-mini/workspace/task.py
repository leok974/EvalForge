class Account:
    def __init__(self, balance: int = 0):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: int):
        # TODO: raise ValueError if amount <= 0, then add to balance
        pass

    def withdraw(self, amount: int):
        # TODO: raise ValueError if amount <= 0 or amount > self._balance, then subtract
        pass
