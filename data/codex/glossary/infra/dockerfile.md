# Dockerfile

## Definition
A **Dockerfile** is a script-like file that describes how to build a Docker image: base image, copied files, installed dependencies, and the default command.

## Tiny example
A typical pattern:
- set `WORKDIR`
- copy dependency files
- install dependencies
- copy source
- set `CMD`

## Common pitfall
Copying the entire source before installing dependencies can make builds slow because caching breaks. Copy dependency files first (like `requirements.txt`) so Docker can cache installs.

## Related
Image, Container
