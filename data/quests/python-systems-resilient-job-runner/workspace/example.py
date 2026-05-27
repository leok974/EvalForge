from __future__ import annotations

# Example: a simple "try-once-with-fallback" pattern.
# Your task implements a more powerful version: exponential backoff with chained errors.


class ServiceUnavailable(Exception):
    pass


def with_fallback(primary_fn: callable, fallback_fn: callable):
    """Try primary; if it raises, use the fallback result instead of retrying."""
    try:
        return primary_fn()
    except Exception:
        return fallback_fn()


# For comparison: a naive fixed-count retry (no backoff, no chaining)
def retry_naive(job: callable, max_attempts: int = 3):
    last_exc = None
    for _ in range(max_attempts):
        try:
            return job()
        except Exception as exc:
            last_exc = exc
    raise RuntimeError("all attempts failed") from last_exc
