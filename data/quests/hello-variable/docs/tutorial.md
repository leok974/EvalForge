# Tutorial: Variables and Strings

## What is a variable?

A variable is a named container for a value. Once you assign a value to a name,
you can use that name anywhere in your program to refer to the value:

```python
greeting = "Hello"
print(greeting)
```

Output:
```
Hello
```

Python sees `greeting`, looks up the value stored under that name, and passes it
to `print()`. Notice we print the *variable name*, not the string literal — this
is the key habit this quest builds.

## String type: text wrapped in quotes

A **string** is a sequence of characters. In Python, strings are wrapped in
quotes — either single (`'...'`) or double (`"..."`):

```python
message = "System ready"
status = 'All clear'
```

Both are valid. Strings can contain spaces, letters, digits, and most symbols.

## Assignment with =

The `=` operator assigns a value to a variable name:

```python
x = 42        # integer
label = "OK"  # string
```

The name goes on the left, the value on the right. You can reassign a variable
at any point — the name simply points to the new value.

## Printing a variable

Pass the variable name directly to `print()`:

```python
status = "Ready"
print(status)   # prints: Ready
```

This is different from `print("status")` — with quotes you would print the
literal word "status", not the value stored in the variable.
