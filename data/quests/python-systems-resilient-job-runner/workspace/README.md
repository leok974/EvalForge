# Resilient Job Runner

Implement `run_with_retry(fn, max_retries)`.
Executes `fn()`. If it raises exception, retry up to `max_retries`.
If all fail, raise the last exception.