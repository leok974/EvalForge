#!/bin/sh
set -eu

# Setup structure
mkdir -p sandbox/archive/2026/

# Copy invoice
cp fixtures/invoice.txt sandbox/archive/2026/invoice.txt

# Copy README to sandbox root
cp fixtures/readme.md sandbox/README.md
