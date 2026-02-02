---
id: glossary/python/syntax-error
title: SyntaxError
section: Glossary
world: Python
---

# SyntaxError

A **SyntaxError** occurs when Python's parser encounters code that doesn't follow the language's grammar rules. The interpreter cannot understand the code, so execution cannot begin.

## Common Causes

### Missing Colon
```python
if x > 5  # ❌ Missing :
    print("Big")
```

### Incorrect Indentation
```python
def greet():
print("Hello")  # ❌ Not indented
```

### Unmatched Brackets
```python
result = (1 + 2  # ❌ Missing )
```

### Invalid Assignment
```python
5 = x  # ❌ Can't assign to literal
```

## Error Message Example

```
  File "script.py", line 3
    if x > 5
           ^
SyntaxError: invalid syntax
```

The `^` points to where Python detected the issue (though the actual error might be earlier).

## Fixing SyntaxErrors

1. **Read the error carefully**: Check the line number
2. **Look before the marked line**: The error might be earlier  
3. **Check for missing characters**: `:`, `)`, `]`, `}`
4. **Verify indentation**: Use consistent spaces/tabs
5. **Match quotes**: Ensure strings are properly closed

## Prevention Tips

- Use a good code editor with syntax highlighting
- Enable linting (e.g., `pyright`, `flake8`)
- Test code frequently in small chunks
- Follow PEP 8 style guidelines

## Related Errors

- **IndentationError**: Wrong indentation level
- **TabError**: Mixed tabs and spaces  
- **NameError**: Variable not defined (runtime, not syntax)
