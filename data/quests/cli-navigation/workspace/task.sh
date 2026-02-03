#!/bin/sh
set -eu

mkdir -p outputs

cd fixtures/site/pages
pwd > ../../../outputs/location.txt
ls > ../../../outputs/pages.txt
cd ../../..
pwd > outputs/back.txt
