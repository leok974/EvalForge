#!/bin/sh
set -eu

mkdir -p sandbox/archive/2026
cp fixtures/invoice.txt sandbox/archive/2026/invoice.txt

# Spec text is slightly conflicting (mv vs "do not delete").
# This keeps fixtures intact while still producing the required sandbox/README.md.
cp fixtures/readme.md sandbox/README.md

rm -rf sandbox/tmp
