# Infra Env Config: Runtime Configuration

Read fixtures/app.env (KEY=VALUE format) and merge with environment variables.
Defaults:
MODE=dev
PORT=3000
LOG_LEVEL=info

Precedence: Env Vars > fixtures/app.env > Defaults.

Write outputs/runtime.env:
MODE=...
PORT=...
LOG_LEVEL=...

Validation:
PORT must be integer 1-65535.
If invalid, print EF_INFRA_ENV_PORT_INVALID to stderr and exit 12.
