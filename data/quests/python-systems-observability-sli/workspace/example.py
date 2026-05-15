import math


def _is_success(status) -> bool:
    return isinstance(status, int) and 200 <= status <= 399


def _is_5xx(status) -> bool:
    return isinstance(status, int) and 500 <= status <= 599


def _p95(latencies: list[int]) -> int:
    if not latencies:
        return 0
    xs = sorted(latencies)
    k = math.ceil(0.95 * len(xs))
    return xs[k - 1]


def compute_sli_report(events: list[dict]) -> dict:
    total = len(events)
    if total == 0:
        return {}
    successes = sum(1 for e in events if _is_success(e.get("status")))
    errors_5xx = sum(1 for e in events if _is_5xx(e.get("status")))
    latencies = [e["latency_ms"] for e in events if "latency_ms" in e]

    route_data: dict[str, dict] = {}
    for e in events:
        r = e.get("route", "unknown")
        d = route_data.setdefault(r, {"requests": 0, "errors_5xx": 0, "latencies": []})
        d["requests"] += 1
        if _is_5xx(e.get("status")):
            d["errors_5xx"] += 1
        if "latency_ms" in e:
            d["latencies"].append(e["latency_ms"])

    routes = sorted([
        {"route": r, "requests": d["requests"], "errors_5xx": d["errors_5xx"],
         "avg_latency_ms": round(sum(d["latencies"]) / len(d["latencies"])) if d["latencies"] else 0}
        for r, d in route_data.items()
    ], key=lambda x: x["route"])

    success_rate = round(successes / total, 3)
    error_rate = round(errors_5xx / total, 3)
    p95 = _p95(latencies)
    return {
        "total_requests": total,
        "success_rate": success_rate,
        "error_rate": error_rate,
        "p95_latency_ms": p95,
        "slo_ok": success_rate >= 0.99 and p95 <= 200,
        "routes": routes,
    }
