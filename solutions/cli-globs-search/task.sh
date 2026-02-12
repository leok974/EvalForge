#!/bin/sh
set -eu

mkdir -p outputs

# Count lines containing ERROR across all .log files
# Use cat | grep to avoid filename prefixes (safer than grep -h)
count="$(cat fixtures/*.log 2>/dev/null | grep "ERROR" | wc -l | tr -d '[:space:]')"
echo "$count" > outputs/error_count.txt

# List filenames (no dirs) that contain at least one ERROR
{
  for f in fixtures/*.log; do
    if [ -f "$f" ] && grep -q "ERROR" "$f"; then
      basename "$f"
    fi
  done
} | sort > outputs/error_files.txt
