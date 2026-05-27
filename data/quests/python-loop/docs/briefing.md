# Mission: The Control Loop

Automation is the art of performing repetitive tasks with perfect consistency. In Python, the `for` loop lets you iterate through a range of numbers and collect results into a list.

### Your Objective

Implement `generate_evens(limit: int) -> list[int]` in `main.py`:

- Accept an integer `limit`.
- Return a **list** of all even integers from `2` to `limit` inclusive, in ascending order.
- If there are no even integers in that range, return an empty list.

### Expected Input / Output

```python
generate_evens(10)  # → [2, 4, 6, 8, 10]
generate_evens(5)   # → [2, 4]
generate_evens(2)   # → [2]
generate_evens(1)   # → []
```

The function must **return** the list — the grader checks the return value, not printed output.

> **Tip:** See `example.py` for a worked example of the same pattern applied to odd numbers.
