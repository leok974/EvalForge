---
id: glossary/web/html/debug-validate
title: Debug Validate
world: web
level: beginner
tags: [validation, debugging, quality]
related:
  - codex:glossary/node/health-checks
  - codex:glossary/node/lockfiles
---

# Debug Validate

## Definition
Validation is a fast, repeatable way to catch broken content/config before runtime. In a mono-repo, a "validate" command typically checks schemas, required files, and link integrity.

## Usage
- Run validation before committing or seeding content.
- Use "fast" mode locally, "strict" mode in CI.
- Prefer clear errors over silent fallbacks.

## Example
```bash
# Example shape (your repo commands may differ)
python scripts/validate_all.py --fast
```

## Pitfalls

* "Warnings only" validation lets regressions leak into main.
* Validators must point to the same source-of-truth as the app.

## Related

* Health Checks: both catch errors before production.
* Lockfiles: both ensure reproducible builds.