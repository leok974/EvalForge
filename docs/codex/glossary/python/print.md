---
id: glossary/python/print
title: Print
world: python
level: beginner
tags: [basics, output, function]
related:
  - codex:glossary/python/variable
---

## Definition
The `print()` function sends data to the standard output (usually your terminal/console). It is the most common way to display information from your program.

## Usage
- Pass one or more arguments to print them.
- Arguments are separated by spaces by default.
- Automatically adds a newline at the end.

## Example
```python
print("Hello World")

name = "Alice"
print("Welcome,", name)
# Output: Welcome, Alice
```

## Tips
- You can print multiple items: `print(a, b, c)`
- You can format strings using f-strings: `print(f"Value: {x}")`
