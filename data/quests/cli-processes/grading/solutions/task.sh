#!/bin/sh
set -eu
mkdir -p outputs

# Skip header, sort by CPU (col2) numeric desc, take first line as-is.
tail -n +2 fixtures/ps.txt \
  | sort -k2,2nr \
  | head -n 1 > outputs/top_process.txt
