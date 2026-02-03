#!/bin/sh
set -eu
mkdir -p outputs

# Skip header, sort by CPU (col2) desc numeric, take first, print cols 1-3
tail -n +2 fixtures/ps.txt \
  | sort -k2,2nr \
  | head -n 1 > outputs/top_cpu.txt
