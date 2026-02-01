# Interpreter

**Definition**: A program that reads and executes your code line by line, translating it into machine instructions.

## What it does

The Python interpreter:
- Reads your `.py` file
- Parses the syntax (checks if code is valid Python)
- Executes instructions one by one
- Shows output or errors

## How it works

```python
# You write code
print("Hello")

# Interpreter translates to machine instructions
# Output appears: Hello
```

## Common encounters

- **Error messages**: The interpreter tells you what went wrong
- **Interactive mode**: Type code directly (REPL)
- **Script mode**: Run a whole file with `python script.py`

## Key insight

The interpreter must be able to **parse** your code before it can run it. Syntax errors stop the interpreter immediately — it won't execute any code if it can't understand the structure.

## Related
- [SyntaxError](python/syntax-error)
- [REPL](python/repl)
