# Observability & Tracing

If you can’t explain what the agent did, you can’t trust it.

---

## Minimum observability

Every run should produce:
- run_id
- step list
- tool calls (inputs/outputs)
- timings
- final status (success/fail/budgeted)
- artifact links (diffs, reports)

---

## Useful metrics

- runs_total (by status)
- verification_failures_total
- retries_total
- tool_time_ms buckets
- cost_estimate
- approval_required_total

---

## Debugging workflow

1) Find run_id
2) Inspect steps
3) Inspect tool failures
4) Inspect verification evidence
5) Re-run smallest failing step
