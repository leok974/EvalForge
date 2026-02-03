# Images & Containers

Edit task.sh so it creates:

1) outputs/definitions.txt with EXACTLY these keys:
IMAGE=...
CONTAINER=...
BUILD_VS_RUN=...

2) outputs/commands.txt with EXACTLY these keys:
BUILD=...
RUN=...

Rules:
- Keep definitions short (one line each).
- Definitions must include the keywords:
  IMAGE: "template"
  CONTAINER: "running"
  BUILD_VS_RUN: "build" and "run"
- Commands must start with `docker build` and `docker run`.
