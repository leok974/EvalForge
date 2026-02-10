#!/bin/sh
set -eu
mkdir -p outputs
printf "MODE=dev\nPORT=3000\nLOG_LEVEL=info\n" > outputs/runtime.env
