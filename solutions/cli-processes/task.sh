#!/bin/sh
set -eu

mkdir -p outputs

# Extract PIDs whose line contains "python" (skip header)
# Sort explicitly to meet contract
awk 'NR>1 && $0 ~ /python/ { print $1 }' fixtures/ps.txt | sort > outputs/pids.txt
