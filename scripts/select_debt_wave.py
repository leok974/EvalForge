"""
scripts/select_debt_wave.py
Selects a wave of quests from DEBT_REMAINING_67.json for backfilling.

Usage:
    python scripts/select_debt_wave.py --n 20 --order python,sql,js,ts --wave 1
    → docs/audits/DEBT_WAVE_01.json
"""
import argparse
import json
from pathlib import Path

DEBT_FILE = Path("docs/audits/DEBT_REMAINING_67.json")

WORLD_PRIORITY_DEFAULTS = [
    "world-python",
    "world-sql",
    "world-js",
    "world-typescript",
    "world-git",
    "world-infra",
    "world-docker",
    "world-agents",
    "world-ml",
    "world-react",
    "unknown",
]

# Map CLI shorthand → world_id
WORLD_MAP = {
    "python":     "world-python",
    "sql":        "world-sql",
    "js":         "world-js",
    "node":       "world-js",
    "ts":         "world-typescript",
    "typescript": "world-typescript",
    "git":        "world-git",
    "infra":      "world-infra",
    "docker":     "world-docker",
    "agents":     "world-agents",
    "ml":         "world-ml",
    "react":      "world-react",
}

def main():
    parser = argparse.ArgumentParser(description="Select a debt-reduction wave from the frozen list.")
    parser.add_argument("--n", type=int, default=20, help="Max quests to include in wave")
    parser.add_argument("--order", type=str, default="python,sql,js,ts",
                        help="Comma-separated world shorthands (priority order)")
    parser.add_argument("--wave", type=int, default=1, help="Wave number")
    parser.add_argument("--input", type=str, default=str(DEBT_FILE), help="Path to debt freeze JSON")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    quests = data["quests"]

    # Build ordered world list
    world_order = []
    for part in args.order.split(","):
        part = part.strip()
        mapped = WORLD_MAP.get(part, part)
        if mapped not in world_order:
            world_order.append(mapped)
    # Append remaining worlds not specified
    for w in WORLD_PRIORITY_DEFAULTS:
        if w not in world_order:
            world_order.append(w)

    def sort_key(q):
        world_rank = world_order.index(q["world"]) if q["world"] in world_order else 999
        return (world_rank, q["missing_count"])

    sorted_quests = sorted(quests, key=sort_key)
    wave_quests = sorted_quests[: args.n]

    wave_num = f"{args.wave:02d}"
    out_path = Path(f"docs/audits/DEBT_WAVE_{wave_num}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    wave_data = {
        "wave": args.wave,
        "n": len(wave_quests),
        "world_order": world_order,
        "quests": wave_quests,
    }
    out_path.write_text(json.dumps(wave_data, indent=2), encoding="utf-8")

    # Summary
    from collections import Counter
    by_world = Counter(q["world"] for q in wave_quests)
    print(f"✅ Wave {args.wave}: Selected {len(wave_quests)} quests → {out_path}")
    print("\nBy World:")
    for w in world_order:
        if w in by_world:
            print(f"  {w}: {by_world[w]}")
    print("\nSlug list:")
    for q in wave_quests:
        print(f"  [{q['world']}] {q['slug']}  — missing: {', '.join(q['missing_fields'])}")

if __name__ == "__main__":
    main()
