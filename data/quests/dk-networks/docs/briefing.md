# Networks

By default, Docker Compose puts all services on a single default network and they can reach each other by service name. But as stacks grow, you need **named networks** to:

- Isolate groups of services from each other
- Control which services can communicate
- Make intent explicit in code

## Your Task

Update `compose.yaml` to:

1. Connect the `api` service to a named network called `backend`
2. Connect the `db` service to the same `backend` network
3. Declare the `backend` network at the top level

With this setup, `api` can reach `db` via hostname `db` (the service name), but `db` is not exposed to any other networks.
