# Observability & SLIs

## Objective
Read a small set of request log events from a fixture file, compute a deterministic SLI report, and print it as canonical JSON.

This quest trains observability fundamentals:
- turning raw events into measurable SLIs
- separating IO boundary (read/print) from core computation
- deterministic metrics output (stable rounding + stable ordering)

## Input
A JSON array of events in:
- `fixtures/events.json`

Each event object has:
- `ts` (string): ISO-like timestamp (not used for math here)
- `route` (string): endpoint name
- `status` (int): HTTP status code
- `latency_ms` (int): request latency in milliseconds

## Output
Print exactly one line to stdout: a JSON object using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

## Metrics to Compute (Global)
Compute these global SLIs across all events:
- `total_requests` (int)
- `success_rate` (float): successes / total, where success = 2xx or 3xx
- `error_rate` (float): errors / total, where error = 5xx
- `p95_latency_ms` (int): 95th percentile latency (nearest-rank method)
- `slo_ok` (bool): true if:
  - success_rate >= 0.90
  - p95_latency_ms <= 250

## Per-Route Metrics
For each unique route, compute:
- `requests` (int)
- `errors_5xx` (int)
- `avg_latency_ms` (int): rounded to nearest int

The `routes` list must be sorted by route name ascending.

## Percentile Definition
Use the nearest-rank method:
- Sort latencies ascending
- Let k = ceil(0.95 * N)
- p95 = value at index (k-1)

## Rounding Rules
- success_rate and error_rate must be rounded to 3 decimals
- avg_latency_ms rounded to nearest int

## Constraints
- Standard library only.
- Core computation must not read files or print.
- Only `main.py` may read the fixture and print stdout.
- Deterministic behavior only (no time-based randomness).

## Verification
Locally:
```bash
python main.py
```

You should see one canonical JSON line printed.
