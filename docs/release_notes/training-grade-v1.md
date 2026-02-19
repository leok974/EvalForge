# Release Notes: Training-Grade v1.0

**Date**: 2026-02-19
**Tag**: `training-grade-v1`
**Commit**: `phase-l-ratchet`

## Highlights
- **100% Schema Validation**: All 152 quests now have valid, actionable objectives.
- **Runtime Fallback**: Config errors now trigger safe, strict errors instead of Coach hallucinations.
- **Regression-Proof CI**: New comprehensive test suite (Fuzzing, Drift, Smoke, Parity).
- **Golden Ratchet System**: Quality is now enforced by CI budgets constraints.

## Metrics (Snapshot)
- **Total Quests**: 152
- **Golden Run (🥇)**: 54
- **Golden State (🥈)**: 58
- **Golden Spec (🥉)**: 40 (Capped)

## Known Blockers (Spec Tier)
The following quest groups remain in 'Spec' tier (legacy validation) and are scheduled for upgrade:
- `cli-globs-search`
- `cli-ignition`
- `react-*` (React quests waiting for browser runner)
- `cli-*` (Complex interactive patterns)

## CI Gates
This release enforces the following gates on every commit:
1. `objectives_schema`: No invalid objectives allowed.
2. `golden_coverage`: No regression in Golden Tier counts.
3. `drift_check`: Code must match Golden State definitions.
4. `ratchet_budget`: Spec count cannot exceed 40.
