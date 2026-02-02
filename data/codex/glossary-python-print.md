---
id: glossary/python/print
title: print() Function
section: Glossary
world: Python
---

# print() Function

The `print()` function outputs text and data to the console, making it one of the most essential tools for debugging and displaying results.

## Basic Usage

```python
print("Hello, World!")
# Output: Hello, World!
```

## Multiple Arguments

```python
print("Score:", 100, "Gold:", 50)
# Output: Score: 100 Gold: 50
```

## Separator and End

```python
print("A", "B", "C", sep="-")
# Output: A-B-C

print("Loading", end="...")
print("Done")
# Output: Loading...Done
```

## Formatting

```python
name = "Agent"
level = 5
print(f"{name} reached level {level}")
# Output: Agent reached level 5
```

## Common Use Cases

- **Debugging**: Check variable values
- **User Output**: Display results and messages
- **Logging**: Track program flow

## Key Parameters

- `sep`: String inserted between values (default: `' '`)
- `end`: String appended after output (default: `'\n'`)  
- `file`: Where to write (default: `sys.stdout`)
