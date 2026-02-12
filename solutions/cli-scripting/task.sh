#!/bin/sh
set -eu

name="${1:-}"

# Check if name has at least one non-whitespace char
if echo "$name" | grep -q "[^[:space:]]"; then
  echo "Hello, $name!"
  exit 0
else
  echo "Usage: task.sh <name>"
  exit 1
fi
