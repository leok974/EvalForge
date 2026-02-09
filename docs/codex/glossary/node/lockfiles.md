---
id: glossary/node/lockfiles
title: Lockfiles
world: node
level: beginner
tags: [dependencies, package-management, reproducibility]
related:
  - codex:glossary/node/health-checks
  - codex:glossary/web/html/debug-validate
---

# Lockfiles

## Definition
A lockfile pins exact dependency versions so installs are reproducible across machines and CI. Examples include `package-lock.json`, `pnpm-lock.yaml`, and `yarn.lock`.

## Usage
- Commit lockfiles to ensure deterministic builds.
- CI should install from the lockfile.
- Helps avoid "works on my machine" dependency drift.

## Example
```bash
# npm
npm ci

# pnpm
pnpm install --frozen-lockfile

# yarn
yarn install --frozen-lockfile
```

## Pitfalls

* Mixing package managers can cause churn and inconsistent installs.
* Editing lockfiles manually is risky—regenerate via the tool.

## Related

* Health Checks: both are part of production readiness.
* Debug Validate: validation ensures dependencies are correct.