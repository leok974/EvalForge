# Briefing — Resilient Job Runner

## Objective
Run a batch of jobs from `fixtures/jobs.json` with bounded retries and emit a deterministic JSON report.

## What This Trains
- Retry policy: bounded attempts, retryable vs non-retryable errors
- Deterministic outcomes (stable ordering, stable attempt counts)
- Clean boundaries (core runner does not do IO)

## Success Criteria
- Output JSON deep-equals the expected report.
- Transient failures retry up to 3 attempts.
- Fatal failures do not retry.
- One canonical JSON line to stdout, nothing else.
