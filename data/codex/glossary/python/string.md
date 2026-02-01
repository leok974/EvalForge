# String

**Definition**: Text data enclosed in quotes.

## Syntax

```python
# Single quotes
name = 'Alice'

# Double quotes (equivalent)
message = "Hello, world!"

# Triple quotes (multi-line)
story = """
Once upon a time
there was a coder
"""
```

## Common operations

```python
# Concatenation
greeting = "Hello" + " " + "world"  # "Hello world"

# Repetition
laugh = "ha" * 3  # "hahaha"

# Length
len("hello")  # 5

# Indexing
word = "Python"
word[0]  # 'P'
word[-1]  # 'n'
```

## Common mistakes

- **Unmatched quotes**: `print("hello)` → SyntaxError
- **Mixing quote types mid-string**: `name = 'Bob"` → SyntaxError
- **Forgetting escape**: `path = "C:\new"` → `\n` is a newline, use `r"C:\new"` or `"C:\\new"`

## Key insight

Strings are **immutable** — you can't change them in place. Operations like `+` or `.replace()` create new strings.

## Related
- [print()](python/print)
- [f-strings](python/f-strings)
- [SyntaxError](python/syntax-error)
