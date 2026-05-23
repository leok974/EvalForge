# Tutorial: Defensive File Handling

Defensive programming is the practice of anticipating and handling potential errors before they crash your application. This is especially important for File I/O.

## Checking Existence
Always verify a file exists before trying to open it.

```python
from pathlib import Path

p = Path("config.txt")
if not p.exists():
    print("Warning: File not found")
```

## Try / Except / Finally
The standard way to handle errors in Python is the `try-except` block.

```python
try:
    with open("data.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File missed!")
```

## Parsing Strings
When reading configuration files, you often need to split strings by a delimiter like `=`.

```python
line = "api_key = 12345"
key, val = line.split("=", 1)  # Limit split to 1 to handle '=' in values
print(key.strip())  # "api_key"
```

## Returning Defaults
When an error occurs, it's often better to return a "null" or "empty" value (like `None` or `{}`) so the rest of the application can continue running.
