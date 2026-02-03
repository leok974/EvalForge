#!/bin/sh
set -eu

mkdir -p sandbox/archive/2026

cp fixtures/invoice.txt sandbox/archive/2026/invoice.txt

# Correcting solution to CP instead of MV to satisfy "fixtures preserved" rule
cp fixtures/readme.md sandbox/README.md

rm -rf sandbox/tmp
