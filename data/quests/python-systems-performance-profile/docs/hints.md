# Hints: Performance & Profiling

## Hint 1 — Concept

Use the pre-defined `_TOKEN_RE` regex (already in the stub) to extract tokens, then lowercase them:

```python
tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
```

`_TOKEN_RE` matches contiguous alphabetic sequences, so digits and punctuation act as separators. `"hello123world"` → `["hello", "world"]`.

## Hint 2 — Guided

Use `Counter` from `collections` to count all token occurrences in one call:

```python
from collections import Counter
counts = Counter(tokens)
```

`counts.items()` yields `(token, count)` pairs ready to sort.

## Hint 3 — The Solution

Sort by count descending, then alphabetically ascending on tie, then slice to k:

```python
return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
```

Full function:

```python
def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    counts = Counter(tokens)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
```
