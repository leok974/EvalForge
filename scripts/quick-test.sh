#!/bin/bash
# Pre-commit hook or manual "quick test"
# Usage: ./scripts/quick-test.sh

echo "ðŸ§™ Running targeted tests..."
changed_tests=$(git diff --cached --name-only | grep -E '(.test.tsx?|.test.ts)$' || true)

if [ -n "$changed_tests" ]; then
  echo "Found changed tests: $changed_tests"
  pnpm -C apps/web vitest run $changed_tests || exit 1
else
  echo "No test files changed."
fi
