# print()

**Definition**: A function that writes output to the console/terminal.

## Syntax

```python
print(value1, value2, ...)
```

## Examples

```python
# Simple string
print("Hello, world!")

# Multiple values (auto-spaced)
print("Score:", 42)  # Score: 42

# Variables
name = "Alice"
print("Hello,", name)  # Hello, Alice

# Custom separator
print("a", "b", "c", sep="-")  # a-b-c

# No newline at end
print("Loading", end="...")  # Loading...
```

## Common mistakes

- **Python 2 vs 3**: In Python 2, `print "hello"` worked. In Python 3, you MUST use `print("hello")` with parentheses.
- **Mixing types without str()**: `print("Age: " + 25)` → TypeError. Use `print("Age:", 25)` or `print("Age: " + str(25))`

## Why it matters

`print()` is your primary debugging tool. Use it to:
- Check variable values
- Trace execution flow
- Verify output matches expectations

## Quick tips

```python
# Debug variable state
x = 10
print(f"DEBUG: x = {x}")

# Show execution reached a point
print("Made it to line 42")

# Pretty print complex data
from pprint import pprint
pprint({"key": "value", "nested": [1, 2, 3]})
```

## Related
- [String](python/string)
- [f-strings](python/f-strings)
- [stdout](python/stdout)
