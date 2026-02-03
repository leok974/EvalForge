#!/bin/sh
set -eu
mkdir -p outputs

# overwrite with header
echo "HEADER" > outputs/report.txt
# append data
cat fixtures/data.txt >> outputs/report.txt
# append footer
echo "FOOTER" >> outputs/report.txt
