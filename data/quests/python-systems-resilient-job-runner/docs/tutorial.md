# Exponential Backoff and Exception Chaining

Resilience is about handling failure gracefully and providing enough context for debugging.

### Calculating Backoff
The standard formula for exponential backoff is `base_delay * (2 ** attempt_index)`. 
Note that `attempt_index` should start at 0 for the first retry (after the first failure).

### Exception Chaining
When raising a custom error due to an underlying failure, use the `from` keyword to preserve the traceback. this is called **Explicit Exception Chaining** (PEP 3134).

```python
try:
    dangerous_operation()
except Exception as e:
    raise MyCustomError("Operation failed") from e
```

### Dependency Injection for Testing
In the `run_with_retries` function, we pass `sleep_fn=time.sleep`. In production, this calls the real system sleep. In tests, we can pass a mock function that merely records the duration without actually waiting, making our tests deterministic and fast.

### Your Task
Implement the `run_with_retries` function. Pay close attention to the `attempt_index` and ensure the original exception is chained to the `RetryError`.
