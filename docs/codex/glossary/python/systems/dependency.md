---
id: glossary/python/systems/dependency
title: Dependency
world: python
level: beginner
tags: [packaging, imports, architecture]
related:
  - codex:glossary/python/systems/pip
  - codex:glossary/python/systems/package-manager
  - codex:glossary/python/systems/module-not-found-error
---

## Definition
A **dependency** is a third-party library or package that your code relies on. In Python, dependencies are typically installed via pip from PyPI and listed in `requirements.txt` or `pyproject.toml`.

## Usage
- Declare dependencies in `requirements.txt` for reproducible installations.
- Pin dependency versions to avoid breaking changes.
- Keep dependencies up-to-date but test upgrades before deploying.

## Example
```bash
# requirements.txt
requests==2.31.0
flask==3.0.0
pytest>=7.4.0

# Install all dependencies
python -m pip install -r requirements.txt

# Show dependency tree
python -m pip show requests
```

## Pitfalls ##
* Unpinned versions (`requests` instead of `requests==2.31.0`) can cause "works locally, breaks in CI" issues.
* Adding too many dependencies increases security surface area and installation time.

## Related

* Pip: pip installs dependencies.
* Package Manager: manages dependencies for your project.
* ModuleNotFoundError: occurs when dependencies aren't installed.