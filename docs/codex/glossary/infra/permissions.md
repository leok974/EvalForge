---
title: Permissions
id: glossary/infra/permissions
world: infra
level: intermediate
tags: [security, filesystem, debugging]
related:
  - codex:glossary/infra/filesystem
  - codex:glossary/infra/shell
---

# Permissions

## Definition
Permissions control who can read/write/execute files. In containers, permission issues often come from UID/GID mismatches between host mounts and container users.

## Usage
- Prefer running as non-root in production.
- Fix ownership for mounted volumes when needed.
- Ensure scripts have execute permission.

## Example
```bash
ls -la
chmod +x scripts/run.sh
id
```

## Pitfalls

* Mounting a Windows folder into Linux containers can cause permission surprises.
* Running everything as root "fixes" issues but increases risk.

## Related

* Filesystem: permissions control filesystem access.
* Shell: shells execute commands with user permissions.