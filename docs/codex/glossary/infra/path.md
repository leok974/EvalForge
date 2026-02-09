---
title: Path
id: glossary/infra/path
world: infra
level: beginner
tags: [filesystem, navigation, debugging]
related:
  - codex:glossary/infra/cwd
  - codex:glossary/infra/filesystem
  - codex:glossary/infra/shell
---

# Path

## Definition
A **path** is a location in a filesystem (`/app/src/index.js`). Containers often have different paths than the host, so you must be explicit about working directories.

## Usage
- Use absolute paths in scripts where possible.
- Set `WORKDIR` in Dockerfiles.
- Use `cwd`/working directory deliberately in runners.

## Example
```bash
docker exec -it <container> pwd
docker exec -it <container> ls -la /app
```

## Pitfalls

* Relative paths depend on current working directory.
* Windows vs Linux path separators differ (`\` vs `/`).

## Related

* Cwd: current working directory defines the base for relative paths.
* Filesystem: paths navigate the filesystem.
* Shell: shells interpret paths.