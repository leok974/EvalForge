---
id: glossary/python/systems/package-manager
title: Package Manager
world: python
level: beginner
tags: [packaging, dependencies, tooling]
related:
  - codex:glossary/python/systems/pip
  - codex:glossary/python/systems/venv
  - codex:glossary/python/systems/module-not-found-error
---

## Definition
A **package manager** is a tool that installs, upgrades, and removes third-party libraries ("packages") for your project. In Python, the most common package manager workflow uses **pip** to install packages from PyPI. Package managers matter because they make dependencies reproducible across machines.

## Usage
- Install a dependency for your project (typically into a virtual environment).
- Pin versions so teammates/CI get the same behavior.
- Upgrade carefully to avoid breaking changes.

## Example
```bash
# create + activate a virtual environment first (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# install packages
python -m pip install requests

# freeze exact versions for reproducibility
python -m pip freeze > requirements.txt

# later: install the same set elsewhere
python -m pip install -r requirements.txt
```

## Pitfalls

* **Installing globally** (no venv) often causes version conflicts between projects.
* Forgetting to **pin versions** can cause "works on my machine" bugs when dependencies update.

## Related

* Pip: the standard Python package installer.
* Venv: virtual environments isolate project dependencies.
* ModuleNotFoundError: common error when packages aren't installed.