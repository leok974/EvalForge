import json

with open("data/tracks.json", "r", encoding="utf-8") as f:
    tracks = json.load(f)

print("JS/TS TRACKS:")
for t in tracks:
    if t.get("world_id") in ["world-js", "world-ts"]:
        print(f"{t.get('id')} (world: {t.get('world_id')})")
