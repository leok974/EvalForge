#!/bin/sh
set -eu
mkdir -p outputs

cat > outputs/definitions.txt <<'EOF'
IMAGE=An immutable template snapshot used to create containers.
CONTAINER=A running instance of an image with config, filesystem, and a process.
BUILD_VS_RUN=Build creates an image; run starts a container from that image.
EOF

cat > outputs/commands.txt <<'EOF'
BUILD=docker build -t myapp .
RUN=docker run --rm -p 8000:8000 myapp
EOF
