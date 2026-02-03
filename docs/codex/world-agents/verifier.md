# Verifier

Verification is the difference between “agentic” and “guessing.”

---

## Verification ladder (best to worst)

1) Automated tests
2) Deterministic checks (grep, checksums, schema validation)
3) Structured queries (DB, API assertions)
4) Manual inspection (diff review)

Try to be at level 1–2 whenever possible.

---

## Independence rule

The verifier should not rely on the generator’s own claims.

Bad: “It looks correct.”
Good: “node --test passed” or “hash matches expected.”

---

## Verification reports

A verifier should output:
- pass/fail
- evidence (logs, test output, diff summary)
- next recommended action
