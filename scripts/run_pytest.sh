#!/usr/bin/env bash
set -euo pipefail

# TODO: Replace with real pytest invocation and JSON output.
mkdir -p reports coverage
pytest -q || { echo '{"failed":1}' > reports/pytest.json; exit 1; }
echo '{"failed":0}' > reports/pytest.json
