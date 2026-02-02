---
id: glossary/python/string
title: String (str)
section: Glossary
world: Python
---

# String (str)

A **string** is a sequence of characters used to represent text in Python. Strings are immutable and one of the most commonly used data types.

## Creating Strings

```python
# Single quotes
name = 'Alice'

# Double quotes  
message = "Hello, World!"

# Triple quotes (multiline)
paragraph = """
This is a
multi-line string.
"""
```

## String Operations

### Concatenation
```python
first = "Hello"
last = "World"
combined = first + " " + last
# Result: "Hello World"
```

### Repetition
```python
echo = "echo! " * 3
# Result: "echo! echo! echo! "
```

### Indexing
```python
word = "Python"
word[0]   # 'P'
word[-1]  # 'n'
```

### Slicing
```python
text = "EvalForge"
text[0:4]   # "Eval"  
text[4:]    # "Forge"
```

## Common Methods

- `.upper()` / `.lower()`: Change case
- `.strip()`: Remove whitespace
- `.replace(old, new)`: Substitute text
- `.split(sep)`: Split into list
- `.join(iterable)`: Join list into string

## F-Strings (Python 3.6+)

```python
level = 10
print(f"You reached level {level}!")
# Output: You reached level 10!
```

## Immutability

Strings cannot be modified in place:

```python
text = "hello"
text[0] = "H"  # ❌ TypeError!

# Instead, create a new string:
text = "H" + text[1:]  # ✅ "Hello"
```
