import os
import glob
import shutil

def cleanup():
    # 1. Delete Orphaned Terms
    # Use absolute paths or correct relative paths
    base = os.getcwd()
    patterns = [
        os.path.join(base, "data/codex/glossary/js/term-*.md"),
        os.path.join(base, "data/codex/glossary/ts/term-*.md")
    ]
    for p in patterns:
        files = glob.glob(p)
        print(f"Scanning {p} -> Found {len(files)} files")
        for f in files:
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

    # 2. Delete Junk Quest
    junk = os.path.join(base, "docs/quests/test-scaffold-quest")
    if os.path.exists(junk):
        try:
            shutil.rmtree(junk)
            print(f"Deleted directory: {junk}")
        except Exception as e:
            print(f"Error deleting {junk}: {e}")
    else:
        print(f"Directory not found: {junk}")

if __name__ == "__main__":
    cleanup()
