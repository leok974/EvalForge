# Briefing — Observability & SLIs

## Objective
Compute a small SLI report from request events and print a canonical JSON metrics object.

## What This Trains
- Converting raw logs into measurable SLIs
- Percentiles (p95) using a precise definition
- Deterministic reporting (stable rounding + stable ordering)
- Clean boundaries: core computation is pure; only main.py does IO

## Success Criteria
- Output JSON deep-equals the expected report.
- Rates are correct and rounded to 3 decimals.
- p95 follows nearest-rank definition.
- Routes are sorted ascending.
