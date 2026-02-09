
import os
import requests
from pathlib import Path

CODEX_ROOT = Path(os.getcwd()) / "docs" / "codex"
API_URL = "http://127.0.0.1:8092/api/codex/index/structure"

def get_disk_files():
    files = []
    for f in CODEX_ROOT.rglob("*.md"):
        files.append(str(f.relative_to(CODEX_ROOT)).replace("\\", "/"))
    return files

def get_api_pages():
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()
        pages = []
        for section in data["sections"]:
            for page in section["pages"]:
                # API IDs might differ slightly from paths, but usually map 1:1
                # API ID: world/section/page-id
                # Disk: world/section/page-id.md OR world/page-id.md
                pages.append(page)
        return pages
    except Exception as e:
        print(f"API Error: {e}")
        return []

def main():
    disk_files = get_disk_files()
    api_struct = get_api_pages()
    
    # Map API output to counts per world
    api_counts = {}
    for p in api_struct:
        w = p['world']
        api_counts[w] = api_counts.get(w, 0) + 1
        
    print(f"--- API Counts per World ---")
    for w, c in sorted(api_counts.items()):
        print(f"{w}: {c}")
        
    print(f"\n--- Disk File Counts ---")
    # Heuristic mapping
    disk_counts = {}
    for f in disk_files:
        parts = f.split("/")
        if len(parts) > 0:
            w = parts[0]
            disk_counts[w] = disk_counts.get(w, 0) + 1
            
    for w, c in sorted(disk_counts.items()):
        print(f"{w}: {c}")

    print("\n--- Summary ---")
    all_disk = set(f.split(".")[0] for f in disk_files)
    # This is rough because API IDs are constructed.
    # But counts should match.
    
    for w in disk_counts:
        d_c = disk_counts.get(w, 0)
        a_c = api_counts.get(w, 0)
        if d_c != a_c:
            print(f"MISMATCH in {w}: Disk={d_c}, API={a_c}")
        else:
            print(f"MATCH in {w}: {d_c}")

if __name__ == "__main__":
    main()
