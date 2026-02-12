from __future__ import annotations

import math
from typing import Any


def _is_success(status: Any) -> bool:
    return isinstance(status, int) and 200 <= status <= 399


def _is_5xx(status: Any) -> bool:
    return isinstance(status, int) and 500 <= status <= 599


def _p95_nearest_rank(latencies: list[int]) -> int:
    if not latencies:
        return 0
    xs = sorted(latencies)
    n = len(xs)
    k = math.ceil(0.95 * n)
    return xs[k - 1]


def compute_sli_report(events: list[dict]) -> dict:
    """
    Pure function: compute a deterministic SLI report from raw events.

    Must not print or read files.
    """
    # TODO: Implement metrics per README.
    #
    # Return shape:
    # {
    #   "total_requests": int,
    #   "success_rate": float,   # rounded to 3 decimals
    #   "error_rate": float,     # rounded to 3 decimals (5xx only)
    #   "p95_latency_ms": int,
    #   "slo_ok": bool,
    #   "routes": [
    #       {"route": str, "requests": int, "errors_5xx": int, "avg_latency_ms": int},
    #       ...
    #   ]
    # }
    return {}
