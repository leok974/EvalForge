# Prompts & Contracts

Agents fail most often because the task was vague.

A **contract** turns “do the thing” into something testable.

---

## Prompt ≠ contract

- Prompt: “Make it better”
- Contract: “Reduce bundle size by 10% and prove via build stats”

Contracts specify:
- Inputs
- Outputs
- Constraints
- Verification
- Safety/approval boundaries

---

## Contract template

**Goal:** …
**Inputs:** …
**Outputs:** …
**Constraints:** …
**Verification:** …
**Rollback:** …

Example:

Goal: Add /ready endpoint  
Inputs: server.js  
Output: endpoint responds 200 only when ready.flag exists  
Constraints: no external deps, deterministic  
Verification: node:test suite passes  
Rollback: revert commit

---

## Good constraints

- allowlist file paths
- forbid destructive ops
- define expected output format (JSON, file, stdout)
- add strict timeouts
