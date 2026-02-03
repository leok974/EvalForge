
import os
import shutil
from pathlib import Path

CLI_SLUGS = [
    "cli-ignition",
    "cli-navigation",
    "cli-files-folders",
    "cli-globs-search",
    "cli-redirection",
    "cli-pipes",
    "cli-env-vars",
    "cli-exit-codes",
    "cli-processes",
    "cli-scripting"
]

DOCS_ROOT = Path("docs/quests")
DATA_ROOT = Path("data/quests")

def migrate():
    print("🚀 Migrating CLI Quests to data/quests Canonical Layout")
    for slug in CLI_SLUGS:
        src = DOCS_ROOT / slug
        dst = DATA_ROOT / slug
        
        if not src.exists():
            print(f"⚠️ Source not found: {src}")
            continue
            
        dst.mkdir(parents=True, exist_ok=True)
        print(f"📂 Processing {slug}...")

        # 1. Migrate grading
        src_grading = src / "grading"
        dst_grading = dst / "grading"
        if src_grading.exists():
            if dst_grading.exists():
                shutil.rmtree(dst_grading)
            shutil.copytree(src_grading, dst_grading)
            print(f"   ✅ Copied grading -> {dst_grading}")
        else:
            print(f"   ⚠️ No grading folder in {src}")

        # 2. Migrate starter -> workspace
        src_starter = src / "starter"
        dst_workspace = dst / "workspace"
        if src_starter.exists():
            if dst_workspace.exists():
                shutil.rmtree(dst_workspace)
            shutil.copytree(src_starter, dst_workspace)
            print(f"   ✅ Copied starter -> workspace")
        else:
            print(f"   ⚠️ No starter folder in {src}")

if __name__ == "__main__":
    migrate()
