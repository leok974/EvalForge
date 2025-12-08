#!/usr/bin/env bash
set -euo pipefail

echo "🧪 Running boss smoke tests..."
# Runs all tests matching the boss smoke pattern roughly
python -m pytest -q tests/backend -k "boss and smoke"
