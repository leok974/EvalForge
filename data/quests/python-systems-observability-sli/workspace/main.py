from __future__ import annotations

import json
from pathlib import Path


def calculate_availability(events: list[dict]) -> float:
    # TODO: count events where 200 <= status_code <= 399 as successes
    # TODO: return round(successes / total, 4)
    raise NotImplementedError("TODO: implement calculate_availability(events)")


def main() -> None:
    here = Path(__file__).resolve()
    quest_root = here.parents[1]
    path = quest_root / "fixtures" / "events.jsonl"

    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))

    availability = calculate_availability(events)
    print(f"availability={availability:.4f}")


if __name__ == "__main__":
    main()
