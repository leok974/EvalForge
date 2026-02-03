#!/bin/sh
set -eu

mkdir -p outputs

# Count ERROR lines across all .log files
count="$(grep "ERROR" fixtures/logs/*.log 2>/dev/null | wc -l | tr -d ' ')"
echo "${count}" > outputs/error_count.txt

# Files containing at least one ERROR (filenames only)
grep -l "ERROR" fixtures/logs/*.log 2>/dev/null \
  | xargs -n 1 basename \
  | sort > outputs/error_files.txt
