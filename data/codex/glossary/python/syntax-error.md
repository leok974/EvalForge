# SyntaxError

**Definition**: Python couldn't parse your code, so execution stops before running anything.

## What it looks like

```
SyntaxError: invalid syntax
  File "main.py", line 3
    print("hello)
                ^
```

## Common causes

1. **Missing quotes**: `print("hello)` → missing closing quote
2. **Missing parentheses**: `print "hello"` → Python 3 requires `()`  
3. **Missing colons**: `if x == 5` → should be `if x == 5:`
4. **Invalid indentation**: mixing tabs/spaces or wrong indent level
5. **Typos in keywords**: `pritn(...)` instead of `print(...)`

## Quick fix checklist

1. Read the error message — it points to the line and column
2. Look for the **first** syntax error (fixing it may reveal others)
3. Check for unmatched brackets, quotes, or parentheses
4. Re-run after each fix

## Why it matters

SyntaxError means the interpreter can't even **understand** your code structure, so it refuses to run. Fix syntax first, then logic.

## Related
- [Interpreter](python/interpreter)
- [IndentationError](python/indentation)
- [print()](python/print)
