# Executor

The executor runs the plan using tools.

---

## Executor rules

1) Never invent tool results.
2) Log every action (inputs + outputs).
3) Prefer deterministic commands.
4) Don’t apply changes without approval if risk is non-trivial.
5) Stop when verification fails repeatedly.

---

## Idempotency

If you run the executor twice, it should:
- not duplicate outputs
- not corrupt state
- overwrite outputs deterministically

Good example: write outputs/report.txt from scratch each time.
Bad example: append endlessly.

---

## Tool hygiene

- set timeouts
- cap retries
- treat non-zero exit codes as signals
