#!/bin/bash
set -eu

mkdir -p outputs sandbox/repo sandbox

# Init repo
cd sandbox/repo
git init -b main
cp ../../fixtures/hello.txt hello.txt
git add hello.txt
git commit -m "init"

# Create bare remote and push
cd ..
git init --bare remote.git
cd repo
git remote add origin ../remote.git
git push -u origin main

# Clone
cd ..
git clone remote.git clone

# Write report
cd ..
cat > outputs/report.json <<EOF
{
  "repo_initialized": true,
  "commit_message": "init",
  "clone_exists": true
}
EOF
