# Briefing: Compose Basics

The `db` service is already defined. Your mission: add an `api` service that depends on it.

## Requirements

- Add an `api` service using image `my-api:latest`
- Map host port `8080` to container port `8080`
- Declare `depends_on: db` so Docker starts the database first

## Why depends_on?

Without `depends_on`, Docker Compose starts services in an arbitrary order. Your API would crash on startup if the database isn't ready. `depends_on` enforces start order.
