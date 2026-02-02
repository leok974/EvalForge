---
id: glossary/python/indentation
title: Indentation
section: Glossary
world: Python
---

# Indentation

In Python, **indentation** (whitespace at the start of a line) is not just for readability—it's part of the syntax. It defines code blocks and structure.

## Why Indentation Matters

Unlike languages that use `{}` braces, Python uses indentation to group statements:

```python
if temperature > 30:
    print("Hot!")      # Indented: part of the if block
    wear_shorts()      # Also indented: part of the if block
print("Done")          # Not indented: outside the if block
```

## Rules

1. **Consistent spacing**: Use 4 spaces per indentation level (PEP 8 standard)
2. **No mixing**: Don't mix tabs and spaces in the same file
3. **Same level = same block**: All statements in a block must align

## Common Structures

### Functions
```python
def greet(name):
    message = f"Hello, {name}!"
    print(message)
    return message
```

### Loops
```python
for i in range(3):
    print(i)
    if i == 1:
        print("Middle!")
```

### Classes
```python
class Player:
    def __init__(self, name):
        self.name = name
    
    def jump(self):
        print(f"{self.name} jumps!")
```

## Common Errors

### IndentationError
```python
def broken():
print("Wrong")  # ❌ Expected an indented block
```

### Inconsistent Indentation
```python
if True:
    print("2 spaces")
      print("4 spaces")  # ❌ Inconsistent!
```

### TabError
```python
# Mixing tabs and spaces
if True:
    print("spaces")
\tprint("tab")  # ❌ TabError!
```

## Best Practices

- **Use spaces, not tabs**: Set your editor to insert 4 spaces per tab
- **Auto-format**: Use tools like `black` or `autopep8`
- **Show whitespace**: Enable invisible characters in your editor
- **Stay consistent**: Pick a convention and stick to it

## Tools

- **Linters**: `flake8`, `pylint` catch indentation errors
- **Formatters**: `black` auto-formats to PEP 8
- **Editor Settings**: Configure tab width = 4 spaces
