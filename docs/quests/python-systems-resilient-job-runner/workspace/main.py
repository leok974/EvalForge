import json
from pathlib import Path

from job_runner import run_jobs


def main() -> None:
    fixture_path = Path("fixtures/jobs.json")
    if not fixture_path.exists():
        fixture_path = Path("workspace/fixtures/jobs.json")

    with open(fixture_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    results = run_jobs(jobs)

    # Determinism: sort by id ascending
    results.sort(key=lambda r: int(r.get("id", 0)))

    print(json.dumps(results, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
