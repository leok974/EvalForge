import json
from pathlib import Path

path = Path("data/questpacks/_tier2/sql_tier2.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data["quests"]:
    if q["slug"] == "sql-t2-boss-data-quality-audit":
        has_select = any(obj["id"] == "source_regex_select" for obj in q["objectives"])
        if not has_select:
            q["objectives"].append({
                "id": "source_regex_select",
                "title": "Uses SELECT",
                "kind": "source_regex",
                "rule_json": {"pattern": "(?i)SELECT"}
            })

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
print("Updated sql_tier2.json")
