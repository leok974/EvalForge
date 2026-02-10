
import os
import frontmatter
from pathlib import Path

WORLD_REACT = Path("d:/EvalForge/docs/codex/world-react")
GLOSSARY_REACT = Path("d:/EvalForge/docs/codex/glossary/react")
GLOSSARY_REACT.mkdir(parents=True, exist_ok=True)

files_to_migrate = [
    "components.md", "context.md", "controlled-inputs.md", "custom-hooks.md",
    "effects.md", "events.md", "lists-and-keys.md", "performance-basics.md",
    "props.md", "routing.md", "state.md"
]

print("🚀 Starting React Migration...")

for filename in files_to_migrate:
    src = WORLD_REACT / filename
    dest = GLOSSARY_REACT / filename
    
    if not src.exists():
        print(f"⚠️ Source missing: {src}")
        continue
        
    # Read Content
    post = frontmatter.load(src)
    content = post.content
    metadata = post.metadata
    
    # Update Metadata for Canonical
    stem = src.stem
    new_id = f"glossary/react/{stem}"
    metadata["id"] = new_id
    metadata["world"] = "react" # Ensure world is set
    
    # Write to Glossary
    with open(dest, "wb") as f:
        frontmatter.dump(post, f)
    print(f"✅ Migrated content to {dest} (ID: {new_id})")
    
    # Write Redirect to Source
    old_id = f"world-react/{stem}"
    redirect_post = frontmatter.Post(
        content="",
        id=old_id,
        redirect_to=new_id
    )
    with open(src, "wb") as f:
        frontmatter.dump(redirect_post, f)
    print(f"🔄 Created redirect at {src} -> {new_id}")

print("🎉 Migration Complete")
