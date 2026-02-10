
import os
import frontmatter
from pathlib import Path

WORLD_NODE = Path("d:/EvalForge/docs/codex/world-node")
GLOSSARY_NODE = Path("d:/EvalForge/docs/codex/glossary/node")
GLOSSARY_NODE.mkdir(parents=True, exist_ok=True)

# Map World File -> Glossary File (to replace)
# world-node file -> glossary/node/ file
MAPPING = {
    "error-handling.md": "async-errors.md",
    "env-vars.md": "env-and-config.md",
    "file-system.md": "fs-and-path.md",
    "http-basics.md": "http-basics.md",
    "middleware.md": "middleware.md",
    "modules.md": "modules-esm-cjs.md",
    "npm.md": "package-json.md",
    "node-test.md": "testing-basics.md",
    "observability.md": "logging.md"
}

# New files (no glossary equivalent yet, just move them)
NEW_FILES = [
    "async-await.md",
    "deploy-basics.md"
]

print("🚀 Starting Node Migration...")

# Phase 1: Overwrite existing glossary placeholders
for world_file, glossary_name in MAPPING.items():
    src = WORLD_NODE / world_file
    dest = GLOSSARY_NODE / glossary_name
    
    if not src.exists():
        print(f"⚠️ Source missing: {src}")
        continue
        
    print(f"Migrating {world_file} -> {glossary_name}")
    
    # Read Source
    try:
        post = frontmatter.load(src)
    except Exception as e:
        print(f"Failed to load {src}: {e}")
        continue

    # Determine Target ID (preserve if exists)
    target_id = f"glossary/node/{dest.stem}"
    if dest.exists():
        try:
            dest_post = frontmatter.load(dest)
            if "id" in dest_post.metadata:
                target_id = dest_post.metadata["id"]
        except:
            pass
            
    # Update Metadata
    post.metadata["id"] = target_id
    post.metadata["world"] = "node"
    
    # Write to Glossary (Overwrite garbage)
    with open(dest, "wb") as f:
        frontmatter.dump(post, f)
    print(f"✅ Overwrote {dest} (ID: {target_id})")
    
    # Write Redirect in Source (world-node/...)
    old_id = f"world-node/{src.stem}"
    redirect_post = frontmatter.Post(
        content="",
        id=old_id,
        redirect_to=target_id
    )
    with open(src, "wb") as f:
        frontmatter.dump(redirect_post, f)
    print(f"🔄 Created redirect at {src} -> {target_id}")

# Phase 2: Move new files
for filename in NEW_FILES:
    src = WORLD_NODE / filename
    dest = GLOSSARY_NODE / filename
    
    if not src.exists():
        continue
        
    try:
        post = frontmatter.load(src)
    except:
        continue

    new_id = f"glossary/node/{src.stem}"
    post.metadata["id"] = new_id
    post.metadata["world"] = "node"
    
    with open(dest, "wb") as f:
        frontmatter.dump(post, f)
    print(f"✅ Moved {filename} to {dest}")
    
    old_id = f"world-node/{src.stem}"
    redirect_post = frontmatter.Post(
        content="",
        id=old_id,
        redirect_to=new_id
    )
    with open(src, "wb") as f:
        frontmatter.dump(redirect_post, f)
    print(f"🔄 Created redirect at {src} -> {new_id}")

# Phase 3: Cleanup remaining placeholders in Glossary
# Files that were NOT updated by Phase 1 or 2
updated_files = set(MAPPING.values()) | set(NEW_FILES) | {"event-loop.md", "runtime-and-process.md"}

for file_path in GLOSSARY_NODE.glob("*.md"):
    if file_path.name in updated_files:
        continue
        
    try:
        post = frontmatter.load(file_path)
        content = post.content.lower()
        if "fundamental concept in general" in content or "usage in general" in content:
            print(f"🧹 Clearing placeholder in {file_path.name}")
            post.content = "# " + (post.metadata.get("title") or file_path.stem.title()) + "\n\nContent currently under development."
            with open(file_path, "wb") as f:
                frontmatter.dump(post, f)
    except:
        pass

print("🎉 Node Migration Complete")
