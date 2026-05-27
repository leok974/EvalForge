# Briefing: Performance & Profiling

## The Mission

Production systems handle massive text streams — log lines, telemetry, user input.
When the volume is high, understanding *which words dominate* becomes a profiling
question as much as a correctness one.

In this mission you will implement `most_common_tokens(text, k)`. It receives a raw
text string and an integer `k`. Your function must:

1. Extract every contiguous alphabetic sequence (A–Z / a–z) using the
   pre-built `_TOKEN_RE` regex.
2. Lowercase all tokens.
3. Count occurrences of each token.
4. Return the top-`k` tokens as a list of `(token, count)` tuples, sorted by
   count descending, then alphabetically ascending on tie.

**Objective:** Implement `most_common_tokens(text: str, k: int) -> list[tuple[str, int]]`.

## Example

```
most_common_tokens("ok ok ERROR error warn error", 3)
# → [("error", 3), ("ok", 2), ("warn", 1)]
```
