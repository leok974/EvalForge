# Internal Tooling & DX

## Objective
Implement a small CLI-style tool that reads a command spec from a fixture file,
executes the requested operation, and prints a canonical JSON result.

This quest trains:
- CLI/tool boundaries (parse inputs, return structured outputs)
- deterministic behavior (stable formatting, stable ordering)
- safe input validation (no crashes, clear error codes)

## Input
A JSON object in:
- `fixtures/tool_request.json`

Shape:
- `tool` (string): "slugify" | "sum" | "unique_sorted"
- `payload` (object): tool-specific input

## Output
Print exactly one line to stdout: a JSON object using canonical formatting:
`json.dumps(out, sort_keys=True, separators=(",",":"))`

Required output shape:
- `tool` (string)
- `ok` (bool)
- `result` (string|number|list|null)
- `error` (string|null)

## Tools
### 1) slugify
Payload:
- `text` (string)

Behavior:
- lowercase
- trim
- collapse internal whitespace to single spaces
- replace spaces with "-"
- remove all characters except a-z, 0-9, and "-"
- collapse multiple "-" into one
- strip leading/trailing "-"

Example:
"  Hello,   World!  " -> "hello-world"

### 2) sum
Payload:
- `numbers` (list of ints)

Behavior:
- return the integer sum

### 3) unique_sorted
Payload:
- `items` (list of strings)

Behavior:
- trim each item
- lowercase each item
- drop empty strings
- unique + sorted ascending

## Errors
If the tool is unknown:
- ok=false, result=null, error="EF_TOOL_UNKNOWN"

If payload is missing/invalid for the tool:
- ok=false, result=null, error="EF_TOOL_BAD_INPUT"

## Constraints
- Standard library only.
- Core logic must not read files or print.
- Only `main.py` may read the fixture and print stdout.
- Deterministic behavior only.

## Verification
Locally:
```bash
python main.py
```

You should see one canonical JSON line printed.
