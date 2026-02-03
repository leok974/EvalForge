#!/bin/sh
set -eu

echo "CWD=$(basename $(pwd))"
echo "FILES=$(find . -maxdepth 1 | wc -l | tr -d ' ')"
echo "OK"
