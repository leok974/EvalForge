# Tutorial: Building Developer Tools (DX)

Developer Experience (DX) is about making tools that are a joy to use. This means your tools should be predictable, robust, and handle messy "human" input with grace.

## Regex for String Cleanup
The `re` module is your best friend when building string utilities.

```python
import re

# Replace everything that isn't a-z or 0-9 with a dash
text = re.sub(r'[^a-z0-9]+', '-', text.lower())
```

## List Processing
When processing lists of configuration items, you often need to "canonicalize" them—ensuring they are consistent.

```python
# Canonicalize: lowercase, trim, unique, sorted
items = sorted(list(set(x.strip().lower() for x in items if x.strip())))
```

## Standardized Error Responses
An internal tool should never just "crash". It should return a machine-readable error that a CLI or UI can display.

```python
def _bad(tool, code):
    return {"tool": tool, "ok": False, "result": None, "error": code}
```
By following these patterns, you build tools that your teammates can rely on.
