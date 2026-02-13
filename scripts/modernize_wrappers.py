import json
from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PACKS = REPO_ROOT / "data" / "questpacks"
MODERN_DIR = DATA_PACKS / "_modern"

MAPPING = {
    "agents_core.json": {"id": "agents_core", "world": "world-agents", "track": "track-agents-core", "title": "Agents Core"},
    "git_core.json": {"id": "git_core", "world": "world-git", "track": "track-git-core", "title": "Git Core"},
    "javascript_core.json": {"id": "javascript_core", "world": "world-javascript", "track": "track-js-core", "title": "JavaScript Core"},
    "typescript_core.json": {"id": "typescript_core", "world": "world-typescript", "track": "track-ts-core", "title": "TypeScript Core"},
    "foundry_python.json": {"id": "python_foundry_core", "world": "world-python", "track": "track-python-foundry", "title": "Python Foundry"},
    "python_systems.json": {"id": "python_systems_core", "world": "world-python", "track": "track-python-systems", "title": "Python Systems"},
    "prism_js.json": {"id": "prism_js_core", "world": "world-prism", "track": "track-prism-js", "title": "Prism JS"},
    "prism_typescript.json": {"id": "prism_ts_core", "world": "world-prism", "track": "track-prism-ts", "title": "Prism TS"},
}

def modernize():
    MODERN_DIR.mkdir(parents=True, exist_ok=True)
    
    for filename, meta in MAPPING.items():
        src = DATA_PACKS / filename
        if not src.exists():
            print(f"Skipping missing {filename}")
            continue
            
        print(f"Modernizing {filename} -> {meta['id']}.json")
        try:
            legacy_data = json.loads(src.read_text(encoding="utf-8"))
        except:
            print(f"Failed to read {filename}")
            continue
            
        quests = []
        if isinstance(legacy_data, list):
            for i, item in enumerate(legacy_data):
                slug = None
                path_str = item.get("quest_path") or item.get("questPath")
                if path_str:
                    slug = path_str.split("/")[-1]
                elif "slug" in item:
                    slug = item["slug"]
                
                if slug:
                    quests.append({
                        "slug": slug,
                        "title": f"Quest {slug.replace('-', ' ').title()}", # generic title
                        "track_id": meta["track"],
                        "order": i + 1,
                        "briefing_md": f"# {slug}\n\nPlaceholder briefing.",
                        "workspace": {"files_from": f"../../quests/{slug}/workspace"},
                        "language": "python" if "python" in meta["id"] else "javascript", # heuristic
                        "content_source": "legacy_wrapper"
                    })
        
        modern = {
            "questpack_id": meta["id"],
            "title": meta["title"],
            "world_id": meta["world"],
            "track_id": meta["track"],
            "quests": quests
        }
        
        dst = MODERN_DIR / f"{meta['id']}.json"
        dst.write_text(json.dumps(modern, indent=4), encoding="utf-8")
        print(f"  Generated {dst.name} with {len(quests)} quests")

if __name__ == "__main__":
    modernize()
