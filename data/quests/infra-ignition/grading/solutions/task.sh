#!/bin/sh
set -eu

mkdir -p outputs

req="$(tr -d '\r' < fixtures/tools.txt | sed '/^$/d')"
inst="$(tr -d '\r' < fixtures/which.txt | sed '/^$/d')"

# Determine missing tools (present in req, absent in inst)
missing=""
for t in $req; do
  echo "$inst" | grep -x "$t" >/dev/null 2>&1 || {
    if [ -z "$missing" ]; then missing="$t"; else missing="$missing,$t"; fi
  }
done

if [ -n "$missing" ]; then
  printf "STATUS=FAIL\nMISSING=%s\n" "$missing" > outputs/preflight.txt
  echo "MISSING_TOOLS" 1>&2
  exit 10
else
  printf "STATUS=OK\nMISSING=\n" > outputs/preflight.txt
  exit 0
fi
