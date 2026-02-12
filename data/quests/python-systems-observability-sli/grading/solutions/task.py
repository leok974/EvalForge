from __future__ import annotations

import json
from pathlib import Path


def calculate_availability(events: list[dict]) -> float:
  total = len(events)
  if total == 0:
    return 1.0
  ok = 0
  for e in events:
    code = int(e["status_code"])
    if 200 <= code <= 399:
      ok += 1
  return round(ok / total, 4)


def main() -> None:
  here = Path(__file__).resolve()
  quest_root = here.parents[2]
  path = quest_root / "fixtures" / "events.jsonl"

  events: list[dict] = []
  for line in path.read_text(encoding="utf-8").splitlines():
    if line.strip():
      events.append(json.loads(line))

  availability = calculate_availability(events)
  print(f"availability={availability:.4f}")


if __name__ == "__main__":
  main()
