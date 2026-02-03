#!/bin/sh
set -eu
mkdir -p outputs

# Normalize to lowercase, count, sort by count desc then name asc, take top 2.
cat fixtures/names.txt \
  | tr '[:upper:]' '[:lower:]' \
  | sort \
  | uniq -c \
  | awk '{print $2 " " $1}' \
  | sort -k2,2nr -k1,1 \
  | head -n 2 > outputs/top.txt
