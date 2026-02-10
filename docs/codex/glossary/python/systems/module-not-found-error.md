---
id: glossary/python/systems/module-not-found-error
title: ModuleNotFoundError
world: python
level: beginner
tags: [errors, imports, debugging]
related:
  - codex:glossary/python/systems/pip
  - codex:glossary/python/systems/venv
  - codex:glossary/python/systems/dependency
---

## Definition
**ModuleNotFoundError** occurs when Python cannot find a module you're trying to import. This usually means the package isn't installed, you're in the wrong virtual environment, or the module name is misspelled.

## Usage
- Check if the package is installed with `pip list`.
- Ensure you activated the correct virtual environment.
- Verify the import statement matches the package name exactly.

## Example
```python
# This raises ModuleNotFoundError if 'requests' isn't installed
import requests

# Error message:
# ModuleNotFoundError: No module named 'requests'

# Fix: Install the package
# python -m pip install requests
```

## Pitfalls

* Installing a package globally but running code in a venv without that package.
* Misspelling the module name (e.g., `import request` instead of `import requests`).

## Related

* Pip: use pip to install missing modules.
* Venv: ensure you're in the correct venv where packages are installed.
* Dependency: missing dependencies cause ModuleNotFoundError.