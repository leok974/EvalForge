#!/bin/sh
set -eu

mkdir -p outputs

# Navigate to target directory
cd fixtures/site/pages

# Write absolute path while inside pages (Corrected to 3 levels up)
pwd > ../../../outputs/location.txt

# List filenames one per line
ls -1 > ../../../outputs/pages.txt

# Return to workspace root
cd ../../../

# Write absolute path of workspace
pwd > outputs/back.txt
