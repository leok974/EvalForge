## Hint 1 — Concept

`n % 2 == 0` is `True` when `n` is even. Use this condition inside your loop to decide which integers to keep. The modulo operator `%` gives the remainder: `4 % 2 == 0` (even), `3 % 2 == 1` (odd).

## Hint 2 — Guided

Use the list-accumulation pattern:

```python
result = []
for n in range(1, limit + 1):
    if n % 2 == 0:
        result.append(n)
return result
```

Initialize the list before the loop, append inside the `if` block, and return after the loop ends.

## Hint 3 — The Solution

```python
def generate_evens(limit: int) -> list[int]:
    result = []
    for n in range(1, limit + 1):
        if n % 2 == 0:
            result.append(n)
    return result
```

Note: the function **returns** the list — it does not print anything. The `main()` function (already in the starter) handles printing.
