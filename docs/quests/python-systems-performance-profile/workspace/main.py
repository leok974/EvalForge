import json
from pathlib import Path

from profiler import profile_membership_case


def main() -> None:
    fixture_path = Path("fixtures/profile_case.json")
    if not fixture_path.exists():
        fixture_path = Path("workspace/fixtures/profile_case.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        case = json.load(f)

    report = profile_membership_case(case)

    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
