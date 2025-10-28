#!/usr/bin/env bash
# Pre-push guard: Block pushes containing tasteos paths
# This runs BEFORE code is pushed to remote repository
set -euo pipefail

echo "🔍 Pre-push check: Scanning for TasteOS paths..."

# Check all files being pushed (compare with remote)
remote="$1"
url="$2"

# Read stdin with from/to refs
while read local_ref local_sha remote_ref remote_sha
do
  if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
    # Branch deletion, allow
    continue
  fi
  
  if [ "$remote_sha" = "0000000000000000000000000000000000000000" ]; then
    # New branch, check all commits
    range="$local_sha"
  else
    # Existing branch, check new commits
    range="$remote_sha..$local_sha"
  fi
  
  # Get all changed files in the range
  files=$(git diff --name-only "$range" 2>/dev/null || git show --name-only --pretty="" "$local_sha" 2>/dev/null || true)
  
  # Check for tasteos violations
  violations=$(echo "$files" | grep -Ei '(^|/)tasteos(/|$)' || true)
  
  if [ -n "$violations" ]; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "❌ PUSH BLOCKED: TasteOS paths not allowed in EvalForge"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "The following files contain 'tasteos' in their path:"
    echo "$violations" | sed 's/^/  • /'
    echo ""
    echo "To fix:"
    echo "  1. Remove TasteOS files from this branch"
    echo "  2. Work on TasteOS in separate repo: D:\TasteOS"
    echo ""
    echo "See .vscode/README_EVALFORGE_CONTRACT.md for details"
    echo ""
    exit 1
  fi
done

echo "✅ No TasteOS violations - push allowed"
exit 0
