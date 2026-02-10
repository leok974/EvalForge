---
id: glossary/python/systems/venv
title: Venv
world: python
level: beginner
tags: [tooling, environment, isolation]
related:
  - codex:glossary/python/systems/pip
  - codex:glossary/python/systems/package-manager
  - codex:glossary/python/systems/dependency
---

## Definition
**Venv** is Python's built-in tool for creating isolated virtual environments. Each venv has its own Python binary and package directory, preventing dependency conflicts between projects. Always use a venv for project work.

## Usage
- Create a new venv with `python -m venv <directory>`.
- Activate it to use its isolated Python/pip.
- Deactivate to return to the global environment.

## Example
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Now pip installs go into .venv, not globally
pip install requests

# Deactivate when done
deactivate
```

## Pitfalls

* Forgetting to activate the venv means packages install globally.
* Committing `.venv/` to git bloats repos; add `.venv/` to`.gitignore`.

## Related

* Pip: install packages inside a venv.
* Package Manager: venvs work with pip to manage dependencies.
* Dependency: venvs isolate project dependencies.