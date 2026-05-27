# Tutorial: Object-Oriented Programming (OOP)

Object-Oriented Programming is a paradigm based on the concept of "objects", which can contain data (attributes) and code (methods).

## Defining a Class
A class is like a blueprint for creating objects.

```python
class Dog:
    def __init__(self, name):
        self.name = name  # An attribute

    def bark(self):       # A method
        print(f"{self.name} says woof!")
```

## The __init__ Method
The `__init__` method is a special method called a constructor. It is automatically executed when you create a new instance of a class. It's usually where you initialize your attributes.

```python
my_dog = Dog("Rex")
```

## Self
The `self` parameter is a reference to the current instance of the class. It is used to access variables that belong to the class. It must be the first argument of any method in the class.

## State Management
In this quest, the "state" of your `Account` is the balance, stored in `self._balance`. Expose it with a `@property` so callers can read `account.balance`:

```python
@property
def balance(self):
    return self._balance

def deposit(self, amount):
    self._balance += amount
```

## Validation
Methods should raise `ValueError` before modifying state if the input is invalid:

```python
def deposit(self, amount):
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    self._balance += amount

def withdraw(self, amount):
    if amount <= 0:
        raise ValueError("Withdraw amount must be positive")
    if amount > self._balance:
        raise ValueError("Insufficient funds")
    self._balance -= amount
```

The overdraft check (`amount > self._balance`) prevents the balance from going negative.
