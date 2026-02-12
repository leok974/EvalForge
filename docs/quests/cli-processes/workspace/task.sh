#!/bin/sh
set -eu

mkdir -p outputs

# TODO:
# - read fixtures/ps.txt
# - ignore header
# - select rows whose COMMAND contains "python"
# - write the PID column only
# - sort ascending
# - output to outputs/pids.txt

echo "TODO" > outputs/pids.txt
