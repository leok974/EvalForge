## Concept
First, filter the incoming list into success vs error counts. Use a dictionary to track aggregates per unique `route`.

## Guided
For the P95, don't forget to sort the latencies list before picking the rank. Use `math.ceil` for the rank calculation as specified in the briefing.

## Full Solution
```python
import math

def compute_sli_report(events: list[dict]) -> dict:
    if not events:
        return {}
    
    total = len(events)
    errors = [e for e in events if 500 <= e.get('status', 0) <= 599]
    latencies = sorted([e.get('latency_ms', 0) for e in events])
    
    # P95 nearest rank
    k = math.ceil(0.95 * total)
    p95 = latencies[k-1]
    
    success_rate = round((total - len(errors)) / total, 3)
    
    return {
        "total_requests": total,
        "success_rate": success_rate,
        "p95_latency_ms": p95,
        "slo_ok": success_rate >= 0.95
    }
```
*Note: Ensure the output matches the exact schema requested in the docstrings.*
