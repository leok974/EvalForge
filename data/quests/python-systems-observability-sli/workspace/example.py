from __future__ import annotations


def compute_error_rate(events: list[dict]) -> float:
    """
    Given a list of HTTP event dicts (each with a 'status_code' key),
    return the fraction of requests that resulted in a 5xx error,
    rounded to 4 decimal places.

    compute_error_rate([{"status_code": 200}, {"status_code": 500}]) -> 0.5
    compute_error_rate([]) -> 0.0
    """
    if not events:
        return 0.0
    total = len(events)
    errors = sum(1 for e in events if e.get("status_code", 0) >= 500)
    return round(errors / total, 4)


if __name__ == "__main__":
    sample = [
        {"status_code": 200},
        {"status_code": 201},
        {"status_code": 500},
        {"status_code": 503},
        {"status_code": 200},
    ]
    rate = compute_error_rate(sample)
    print(f"error_rate={rate:.4f}")
