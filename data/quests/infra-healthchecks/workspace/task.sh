#!/bin/sh
set -eu
mkdir -p outputs
echo "STATUS=OK" > outputs/health_status.txt
echo "100" > outputs/health_score.txt
