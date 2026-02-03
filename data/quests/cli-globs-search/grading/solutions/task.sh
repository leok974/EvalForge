#!/bin/sh
set -eu

mkdir -p outputs

# Count matching lines across all .log files (case-sensitive).
# -h avoids prefixing filenames into the output stream.
count="$(grep -h "ERROR" fixtures/logs/*.log 2>/dev/null | wc -l | tr -d ' ')"
echo "${count}" > outputs/error_count.txt

# List filenames (not paths) that contain at least one ERROR.
# grep -l returns exit 1 when no matches, so guard it.
files="$(grep -l "ERROR" fixtures/logs/*.log 2>/dev/null || true)"
if [ -n "${files}" ]; then
  printf "%s\n" "${files}" | xargs -n 1 basename | sort > outputs/error_files.txt
else
  : > outputs/error_files.txt
fi
