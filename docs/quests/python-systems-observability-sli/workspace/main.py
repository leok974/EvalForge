import json
from pathlib import Path

from sli import compute_sli_report


def main() -> None:
    fixture_path = Path("fixtures/events.json")
    if not fixture_path.exists():
        fixture_path = Path("workspace/fixtures/events.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    report = compute_sli_report(events)

    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
