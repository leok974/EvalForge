# Service Boundaries & Contracts

## Objective
Implement a tiny “service” that processes a batch of request objects from a fixture file and emits a deterministic JSON response.

This quest is about **service boundaries**:
- **Core logic** must be pure and deterministic (no IO).
- **Boundary code** handles reading inputs + printing outputs.

## Input
A JSON array of request objects in:
- `fixtures/requests.json`

Each request has:
- `id` (string or number)
- `action` (string)
- action-specific fields (see below)

## Output
Print exactly **one line** to stdout: a JSON array of response objects using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

The output array must be sorted by `id` ascending.

## Required Response Shape
Each response object must have exactly these keys:
- `id` (int)
- `action` (string)
- `ok` (bool)
- `value` (number|string|null)
- `error` (string|null)

## Supported Actions
### 1) sum
Request fields:
- `numbers`: list of integers

Success:
- `value` = sum of numbers

Failure:
- if `numbers` is missing/not a list/contains non-ints → `ok=false`, `value=null`, `error="EF_BOUNDARY_BAD_INPUT"`

### 2) divide
Request fields:
- `numerator`: int
- `denominator`: int

Success:
- `value` = numerator / denominator (for this quest, the fixture values produce an integer result)

Failure:
- if denominator is 0 → `error="EF_BOUNDARY_DIVIDE_BY_ZERO"`
- if fields missing/wrong types → `error="EF_BOUNDARY_BAD_INPUT"`

### 3) concat
Request fields:
- `parts`: list of strings

Success:
- Trim each part, drop empties, join with a single space.
- Example: ["  hello", "world  ", ""] → "hello world"

Failure:
- if parts missing/not a list/contains non-strings → `error="EF_BOUNDARY_BAD_INPUT"`

## Unknown Action
If `action` is not recognized:
- `ok=false`, `value=null`, `error="EF_BOUNDARY_UNKNOWN_ACTION"`

## Constraints (Service Boundaries)
- Core logic must not read files or print.
- Only `main.py` may read the fixture and print stdout.
- Use standard library only.

## Determinism Rules
- Output sorted by `id` ascending.
- Tags/ordering must be stable.
- No extra stdout besides the single JSON line.

## Verification
Run the quest via EvalForge’s runner (submit/run). Locally, you can run:
```bash
python main.py
```

You should see one JSON line printed.
