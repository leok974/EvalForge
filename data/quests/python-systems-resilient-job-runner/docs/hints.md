## Concept
Use a `while` or `for` loop to track the number of attempts. A `try...except` block inside the loop is essential for catching job failures.

## Guided
If the job succeeds, `return` the result immediately. If it fails, check if you have attempts left. If so, calculate the sleep time: `backoff_seconds * (2 ** attempt_count)`. Increment your counter after EACH failure.

## Full Solution
```python
def run_with_retries(job, *, max_attempts=3, backoff_seconds=0.1, sleep_fn=time.sleep):
    last_err = None
    for i in range(max_attempts):
        try:
            return job()
        except Exception as e:
            last_err = e
            # Don't sleep after the final attempt
            if i < max_attempts - 1:
                sleep_fn(backoff_seconds * (2 ** i))
    
    raise RetryError("Job failed after max attempts") from last_err
```
Observe the use of `raise ... from last_err` to maintain the exception cause.
