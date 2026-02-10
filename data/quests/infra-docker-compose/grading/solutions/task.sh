#!/bin/sh
set -eu
mkdir -p outputs

# Extract service keys:
# 1. Enter "services" block
# 2. Exit on any top-level key
# 3. Capture indented keys (exactly 2 spaces) to avoid nested keys like "image:"
tr -d '\r' < fixtures/docker-compose.yml \
  | awk '
      /^services:/ { in_services=1; next }
      /^[^ \t]/ && !/^services:/ { in_services=0 }
      in_services && /^  [a-zA-Z0-9_-]+:/ {
        # Match exactly 2 spaces at start
        key=$1;
        gsub(/:/,"",key);
        print key
      }
    ' \
  | sort > outputs/services.txt
