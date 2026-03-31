# Regular Expressions (Regex)

Regular Expressions are a powerful Domain Specific Language (DSL) used for pattern matching and text manipulation.

### Basic Syntax in Python
Python's `re` module provides rich support for regex:
```python
import re

# Simple pattern match
pattern = r"\d+"  # Matches one or more digits
text = "Error code 404"
match = re.search(pattern, text)
print(match.group())  # Output: 404
```

### Best Practices
1.  **Use Raw Strings**: Always use `r"..."` to avoid backslash escaping issues.
2.  **Keep it Simple**: Overly complex regex is hard to maintain. Break it down or use comments with `re.VERBOSE`.
3.  **Validation**: Use regex for initial sanitization, but use specialized parsers for complex formats like HTML or JSON.

### Relevance in EvalForge
Regex is essential for building robust **Platform Tooling**, especially when slugifying text or parsing raw system logs.
