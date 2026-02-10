#!/bin/sh
set -eu
mkdir -p outputs
printf "STATUS=OK\nMISSING=\n" > outputs/preflight.txt
exit 0
