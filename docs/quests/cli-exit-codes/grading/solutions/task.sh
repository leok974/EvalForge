#!/bin/sh
set -eu

if grep -w "FAIL" fixtures/input.txt >/dev/null 2>&1; then
  echo "BAD" 1>&2
  exit 5
else
  echo "OK"
  exit 0
fi
