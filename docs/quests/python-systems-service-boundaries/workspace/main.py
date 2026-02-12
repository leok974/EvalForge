import json
from pathlib import Path

from core import handle_request, coerce_id


def main() -> None:
    # Boundary responsibilities:
    # - read inputs (fixtures)
    # - call pure core logic
    # - sort + print canonical JSON

    fixture_path = Path("fixtures/requests.json")
    if not fixture_path.exists():
        # Fallback for some runner contexts
        fixture_path = Path("workspace/fixtures/requests.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        requests = json.load(f)

    responses = []
    for req in requests:
        responses.append(handle_request(req))

    # Determinism: sort by int id ascending
    responses.sort(key=lambda r: int(r.get("id", 0)))

    # Canonical JSON (single line)
    print(json.dumps(responses, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
