#!/bin/sh
set -eu

mkdir -p outputs

# TODO:
# 1) Count ERROR lines across fixtures/*.log and write to outputs/error_count.txt
# 2) List basenames of fixtures/*.log files that contain ERROR, sorted, one per line,
#    and write to outputs/error_files.txt

echo "0" > outputs/error_count.txt
: > outputs/error_files.txt
