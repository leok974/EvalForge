# EvalForge: Training-Grade Release (v1.0)

This release marks the transition of EvalForge to a **Training-Grade** quality standard. It introduces comprehensive schema validation, golden-state enforcement, and regression-proof CI gates.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/leok974/EvalForge.git
   cd EvalForge
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Requires Python 3.11+ and Docker Desktop.*

3. **Check Environment**:
   Ensure Docker is running and `EF_COACH_API_KEY` is set if using Coach features.

## Validation Tools

EvalForge v1 includes strict validation tools to ensure content quality and system stability.

### 1. Quest Validation (`--validate-only`)
When seeding or running quests, use the `--validate-only` flag to check schema conformance without modifying the database.

```bash
python -m arcade_app.force_seed_standard --validate-only
```
*Returns exit code 0 on success, 1 on schema violation.*

### 2. Full CI Suite (`ci_check.py`)
Run the entire regression suite (Schema, Drift, Smoke, Fuzz) locally:

```bash
python scripts/ci_check.py --full
```
This script runs:
- **Schema Audit**: Checks all 152 quests for valid objectives.
- **Drift Check**: Verifies `golden.state.json` matches code logic.
- **Smoke Tests**: Runs representative quests in solution mode.
- **Fuzz Tests**: Validates validator robustness against malformed inputs.

## Golden Methodology & Ratchets

We classify quests into three maturity levels ("Golden Types") based on how their success is verified. The release enforces a strictly tracked budget (Ratchet) to drive conversion toward higher quality tiers.

| Tier | Type | Verification Method | Ratchet Budget (v1) |
|------|------|---------------------|---------------------|
| 🥇 | **Run** | `golden.run.json` (Stdout Capture) | **Min: 54** |
| 🥈 | **State**| `golden.state.json` (Files/Git/AST) | **Min: 58** |
| 🥉 | **Spec** | `golden.spec.json` (Manual/Legacy) | **Max: 40** (Cap) |

*The goal is to shrink **Spec** count to 0 over time.*

### Ratchet Enforcement
The CI pipeline fails if:
1. The number of **Spec** quests exceeds 40.
2. The number of **Run** or **State** quests decreases (regression).

## Release Verification
This release is verified by `TRAINING_GRADE_RELEASE_SNAPSHOT.json` which tracks the exact counts and blocked quests at the time of tagging.
