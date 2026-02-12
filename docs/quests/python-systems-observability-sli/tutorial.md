# Tutorial — Observability & SLIs

## Approach
Treat this as a pipeline:
1) Extract signals (status, latency, route)
2) Compute global SLIs (rates, p95)
3) Compute per-route breakdown
4) Emit deterministic JSON once

## Implementation Plan
1. Count total events.
2. Count successes (2xx/3xx) and errors (5xx).
3. Compute success_rate and error_rate:
   - rate = count / total
   - round to 3 decimals
4. Compute p95:
   - sort latencies
   - k = ceil(0.95*N)
   - p95 = latencies[k-1]
5. Compute per-route metrics:
   - requests, errors_5xx
   - avg_latency_ms (rounded to nearest int)
6. Sort routes list by route name.

## Pitfalls
- Using the wrong percentile definition
- Treating 4xx as “error_rate” (this quest defines error_rate = 5xx only)
- Not sorting routes
- Printing debug text (breaks stdout JSON parsing)
