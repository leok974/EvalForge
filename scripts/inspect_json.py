import json
p = "artifacts/codex-missing.json"
d = json.load(open(p, "r", encoding="utf-8"))
print("Top keys:", list(d.keys()))
for k in ("coverage_by_quest", "missing_by_quest", "by_quest", "quests", "items"):
    if k in d:
        print(f"Found {k}, type={type(d[k]).__name__}, len={len(d[k]) if hasattr(d[k], '__len__') else 'n/a'}")

# Sample one quest
for k in ("coverage_by_quest", "missing_by_quest", "by_quest", "quests", "items"):
    if k in d:
        obj = d[k]
        if isinstance(obj, dict):
            slug, row = next(iter(obj.items()))
            print(f"\nSample slug: {slug}")
            print(f"Row keys: {list(row.keys())}")
            print(f"Row content: {row}")
        elif isinstance(obj, list) and obj:
            row = obj[0]
            print(f"\nSample list row keys: {list(row.keys())}")
        break
