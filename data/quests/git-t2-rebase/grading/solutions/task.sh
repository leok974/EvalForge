#!/bin/sh
set -e
sh ./setup.sh

# Rebase
git rebase main
