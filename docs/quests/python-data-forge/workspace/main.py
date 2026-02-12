import json
from pathlib import Path

def normalize_record(record: dict) -> dict:
    """
    Normalize a single raw record.
    """
    # TODO: Implement normalization rules
    return {}

def main() -> None:
    # 1. Read input
    fixture_path = Path("fixtures/raw_contacts.json")
    if not fixture_path.exists():
        # Fallback for some runner contexts, though workspace should map correctly
        fixture_path = Path("workspace/fixtures/raw_contacts.json")
        
    with open(fixture_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # 2. Process
    normalized = []
    # TODO: Normalize each item in raw_data

    # 3. Sort by ID (ensure int)
    # normalized.sort(key=...)

    # 4. Print Canonical JSON
    # print(json.dumps(normalized, sort_keys=True, separators=(",",":")))
    pass

if __name__ == "__main__":
    main()
