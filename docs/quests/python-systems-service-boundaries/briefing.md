# Briefing — Service Boundaries & Contracts

## Objective
Process a batch of requests from `fixtures/requests.json` and emit a deterministic JSON response list.

## What This Trains
This quest is about designing clean boundaries:
- Core function: `handle_request(req) -> response` (pure, deterministic)
- Boundary code: reads fixture + prints canonical JSON

## Success Criteria
- Output JSON deep-equals the expected response array.
- Output is sorted by id ascending.
- No extra stdout besides the one JSON line.
