---
id: glossary/python/systems/pip
title: Pip
world: python
level: beginner
tags: [packaging, tooling, dependencies]
related:
  - codex:glossary/python/systems/package-manager
  - codex:glossary/python/systems/venv
  - codex:glossary/python/systems/module-not-found-error
---

## Definition
**Pip** is Python's default package installer. It downloads and installs packages from PyPI (Python Package Index) and manages dependencies. Pip comes bundled with Python 3.4+, so you usually already have it.

## Usage
- Install packages with `pip install <package>`.
- Uninstall with `pip uninstall <package>`.
- List installed packages with `pip list` or `pip freeze`.

## Example
```bash
# Install a specific version
python -m pip install requests==2.28.0

# Install from requirements file
python -m pip install -r requirements.txt

# Show package details
python -m pip show requests

# Upgrade pip itself
python -m pip install --upgrade pip
```

## Pitfalls

* Running `pip` directly instead of `python -m pip` can use the wrong Python version.
* Installing without a virtual environment pollutes the global Python environment.

## Related

* Package Manager: pip is Python's package manager.
* Venv: use virtual environments to isolate pip installs.
* ModuleNotFoundError: occurs when pip hasn't installed a required package.