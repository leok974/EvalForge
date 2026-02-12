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
    total = 0
    successes = 0
    errors_5xx_total = 0
    latencies: list[int] = []
    
    # Per route aggregation
    # route -> {requests, errors_5xx, latencies}
    route_stats: dict[str, dict] = {}

    for e in events:
        total += 1
        
        # Extract fields
        status = e.get("status")
        route = e.get("route", "")
        latency = e.get("latency_ms", 0)
        
        # Normalize types
        if not isinstance(route, str):
            route = ""
        if not isinstance(latency, int):
            latency = 0
            
        # Global stats
        if _is_success(status):
            successes += 1
        if _is_5xx(status):
            errors_5xx_total += 1
            
        latencies.append(latency)
        
        # Route stats
        if route not in route_stats:
            route_stats[route] = {"requests": 0, "errors_5xx": 0, "latencies": []}
        
        rs = route_stats[route]
        rs["requests"] += 1
        rs["latencies"].append(latency)
        if _is_5xx(status):
            rs["errors_5xx"] += 1

    # Global Calculations
    if total > 0:
        success_rate = round(successes / total, 3)
        error_rate = round(errors_5xx_total / total, 3)
    else:
        success_rate = 0.0
        error_rate = 0.0
        
    p95 = _p95_nearest_rank(latencies)
    
    slo_ok = (success_rate >= 0.90) and (p95 <= 250)
    
    # Per-route list
    routes_out = []
    sorted_route_names = sorted(route_stats.keys())
    
    for rname in sorted_route_names:
        stats = route_stats[rname]
        r_req = stats["requests"]
        r_err = stats["errors_5xx"]
        r_lats = stats["latencies"]
        
        avg_lat = 0
        if r_req > 0:
            # Round to nearest int
            avg_lat = int(round(sum(r_lats) / r_req))
            
        routes_out.append({
            "route": rname,
            "requests": r_req,
            "errors_5xx": r_err,
            "avg_latency_ms": avg_lat
        })
        
    return {
      "total_requests": total,
      "success_rate": success_rate,
      "error_rate": error_rate,
      "p95_latency_ms": p95,
      "slo_ok": slo_ok,
      "routes": routes_out
    }
