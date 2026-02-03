# CLI Ignition

Edit `task.sh` so running:

  sh task.sh

prints exactly 3 lines:

CWD=workspace
FILES=3
OK

Rules:
- FILES must count only regular files directly under `fixtures/` (not subdirectories).
- Do not hardcode the number; compute it.
- Exit code must be 0 on success.
