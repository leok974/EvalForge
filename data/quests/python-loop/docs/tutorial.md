# Loops and List Accumulation

This quest introduces the pattern of using a `for` loop to **collect** values into a list and **return** that list from a function.

## Writing a Function That Returns a List

A function can build up a collection and hand it back to the caller.

```python
def double_range(limit: int) -> list[int]:
    result = []
    for n in range(1, limit + 1):
        result.append(n * 2)
    return result

double_range(3)  # → [2, 4, 6]
```

Key steps:
1. Initialize an empty list **before** the loop: `result = []`
2. Append items that meet your condition **inside** the loop: `result.append(n)`
3. Return the list **after** the loop exits: `return result`

## Checking for Even Numbers

The modulo operator `%` returns the remainder of division. `n % 2 == 0` is `True` when `n` is evenly divisible by 2.

```python
for n in range(1, 6):
    if n % 2 == 0:
        print(n)  # prints 2, then 4
```

## Inclusive Range

`range(start, stop)` goes up to but **not** including `stop`. To include `limit` itself:

```python
range(1, limit + 1)  # iterates 1, 2, 3, … limit
```

## Your Task

In `main.py`, implement `generate_evens(limit)`:

1. Start with an empty list.
2. Loop through integers from `1` to `limit` inclusive.
3. If the integer is even, append it to the list.
4. After the loop, return the list.

No printing required — `main()` is already provided and handles output. Your job is to make `generate_evens` return the correct list.
