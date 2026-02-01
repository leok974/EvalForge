# Indentation

**Definition**: Whitespace (spaces or tabs) at the start of a line that defines code blocks in Python.

## Why it matters

Unlike most languages that use `{}` braces, Python uses indentation to determine what code belongs together.

## Rules

```python
# Correct: 4 spaces per indent level
def greet(name):
    message = f"Hello, {name}"
    print(message)
    
# Correct: consistent tabs OR spaces
if x > 5:
    print("big")
    print("number")
```

## Common errors

### IndentationError

```python
# BAD: No indent after function definition
def greet():
print("hi")  # IndentationError

# GOOD:
def greet():
    print("hi")
```

### TabError

```python
# BAD: Mixing tabs and spaces
def func():
⇥ print("line 1")  # tab
    print("line 2")  # 4 spaces
# TabError: inconsistent use of tabs and spaces
```

### Unexpected indent

```python
# BAD: Random indent
x = 5
    print(x)  # IndentationError: unexpected indent
```

## Best practices

1. **Use 4 spaces** (PEP 8 standard)
2. **Never mix tabs and spaces** in the same file
3. **Configure your editor** to insert spaces when you press Tab
4. **Be consistent** within a file

## Quick fix

If you get indentation errors:
1. Enable "show whitespace" in your editor
2. Convert all tabs to spaces (or vice versa)
3. Ensure each block level increases by exactly 4 spaces

## Related
- [SyntaxError](python/syntax-error)
- [Code blocks](python/code-blocks)
- [PEP 8](python/pep8)
