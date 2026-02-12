# Hints — Observability & SLIs

## Hint 1
Success = 2xx or 3xx. Error-rate here is 5xx only.

## Hint 2
Nearest-rank p95:
k = ceil(0.95 * N), p95 = sorted_latencies[k-1]

## Hint 3
Make output deterministic:
- sort routes by name
- round rates to 3 decimals
- print canonical JSON once
