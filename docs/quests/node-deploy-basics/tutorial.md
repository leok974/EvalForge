# Deploy Basics: Start Scripts and Health Checks

## Outcome

Make an app deploy-friendly with health and start conventions.

## Core concepts

PORT, start script, graceful shutdown, health checks.

## Mental model

production expects predictability (boot, listen, health, stop).

## Walkthrough

`start` script, `/health`, SIGTERM handling.

## Practice

add shutdown hook that closes server cleanly.

## Common pitfalls

hardcoded ports, ignoring SIGTERM.

## Check yourself

Why is graceful shutdown important?

