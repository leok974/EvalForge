# Tutorial: Counting and Ranking Text Tokens

This quest builds a function that extracts alphabetic tokens from raw text, counts occurrences, and returns the top-k by frequency.

## Step 1 — Extracting Tokens

The stub provides `_TOKEN_RE = re.compile(r"[A-Za-z]+")`, which matches every contiguous alphabetic sequence. Use its `findall` method:

```python
raw = _TOKEN_RE.findall("ok ok ERROR error")
# ["ok", "ok", "ERROR", "error"]
```

Lowercase all tokens so `"ERROR"` and `"error"` count as the same token:

```python
tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
# ["ok", "ok", "error", "error"]
```

Non-alphabetic characters act as separators — digits and punctuation split tokens. `"hello123world"` becomes `["hello", "world"]`.

## Step 2 — Counting with Counter

`Counter` from `collections` counts all occurrences in one step:

```python
from collections import Counter

counts = Counter(tokens)
# Counter({"error": 2, "ok": 2, ...})
```

## Step 3 — Sorting and Taking Top K

`counts.items()` yields `(token, count)` pairs. Sort descending by count, ascending alphabetically on tie:

```python
sorted_items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
```

`-kv[1]` reverses the count (highest first). `kv[0]` breaks ties alphabetically (A before B).

Slice to keep only the top k:

```python
return sorted_items[:k]
```

If `text` is empty, `findall` returns `[]`, `Counter([])` is empty, and the sorted slice is `[]` — no special-casing needed.

## Putting It Together

```python
from collections import Counter

def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    counts = Counter(tokens)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
```
