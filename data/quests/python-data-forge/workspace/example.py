import json
from pathlib import Path


def normalize_record(record: dict) -> dict:
    """Normalize a raw contact record to the canonical schema."""
    return {
        "id": int(record.get("id", 0)),
        "name": str(record.get("name") or "Unknown").strip() or "Unknown",
        "email": record.get("email") or None,
        "phone": record.get("phone") or None,
        "is_active": bool(record.get("is_active", False)),
        "tags": sorted(record.get("tags") or []),
    }


def main() -> None:
    fixture_path = Path("fixtures/raw_contacts.json")
    if not fixture_path.exists():
        fixture_path = Path("workspace/fixtures/raw_contacts.json")

    with open(fixture_path) as f:
        raw_data = json.load(f)

    normalized = sorted(
        [normalize_record(r) for r in raw_data],
        key=lambda r: r["id"]
    )
    print(json.dumps(normalized, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
