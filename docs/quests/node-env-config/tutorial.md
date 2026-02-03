# Environment & Config: .env, process.env, Defaults

## Outcome

Use config safely with required checks and defaults.

## Core concepts

`process.env`, `.env`, required vars, secrets.

## Mental model

env vars are per-process; your app should validate at startup.

## Walkthrough

load PORT, set fallback, validate required key.

## Practice

implement `getEnv(name, { required, default })`.

## Common pitfalls

committing secrets, assuming env var exists.

## Check yourself

What’s the difference between config and secrets?

