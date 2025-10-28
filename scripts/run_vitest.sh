#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-debounce}"
pushd exercises/js >/dev/null
npm ci --silent
npm run -s test
popd >/dev/null
# Collect artifacts Vitest wrote (coverage/coverage-final.json)
# ADK looks only at exit code + coverage file path, so nothing else needed.
