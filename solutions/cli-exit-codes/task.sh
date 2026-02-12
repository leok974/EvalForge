#!/bin/sh
set -eu

if [ -f fixtures/error.flag ]; then
  exit 1
fi
exit 0
