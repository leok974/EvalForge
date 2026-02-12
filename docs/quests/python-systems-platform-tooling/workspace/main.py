import json
from pathlib import Path

from tool import run_tool_request


def main() -> None:
    fixture_path = Path("fixtures/tool_request.json")
    if not fixture_path.exists():
        fixture_path = Path("workspace/fixtures/tool_request.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        req = json.load(f)

    out = run_tool_request(req)

    print(json.dumps(out, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
