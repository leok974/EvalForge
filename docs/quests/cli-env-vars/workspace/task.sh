#!/bin/sh
set -eu

mkdir -p outputs

# TODO:
# Write outputs/config.txt with exactly two lines:
# MODE=<mode>
# PORT=<port>
#
# Rules:
# - MODE defaults to dev if unset/empty
# - PORT defaults to 3000 if unset/empty

echo "MODE=TODO" > outputs/config.txt
echo "PORT=TODO" >> outputs/config.txt
