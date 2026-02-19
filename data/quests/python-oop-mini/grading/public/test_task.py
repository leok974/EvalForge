import pytest
from task import Account

def test_account_init():
    a = Account(100)
    assert a.balance == 100
    a2 = Account()
    assert a2.balance == 0

def test_deposit():
    a = Account(50)
    a.deposit(50)
    assert a.balance == 100
    with pytest.raises(ValueError):
        a.deposit(-10)

def test_withdraw():
    a = Account(100)
    a.withdraw(40)
    assert a.balance == 60
    with pytest.raises(ValueError):
        a.withdraw(1000) # Insufficient
    with pytest.raises(ValueError):
        a.withdraw(-10)
