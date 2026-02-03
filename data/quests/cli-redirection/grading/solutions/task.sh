#!/bin/sh
set -eu
mkdir -p outputs

echo "HEADER" > outputs/report.txt
cat fixtures/data.txt >> outputs/report.txt
echo "FOOTER" >> outputs/report.txt
