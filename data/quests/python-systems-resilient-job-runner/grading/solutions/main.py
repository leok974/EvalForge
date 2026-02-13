def run_with_retry(fn, max_retries=3):
    last_exc = None
    for _ in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
    raise last_exc