import json
from pathlib import Path

def get_file_content(path):
    if not path.exists():
        return f"(File not found: {path})"
    return path.read_text("utf-8")

def main():
    root = Path(".")
    react_core = json.loads((root / "data/questpacks/react_core.json").read_text("utf-8"))
    
    quests = react_core["quests"]
    output = []
    
    # Process all quests except react-ignition (already done)
    # Actually, let's just do the next 3 to keep it manageable as requested ("Batch max 2-3")
    # Or dump all to a file. Let's dump all to a file.
    
    count = 0
    for q in quests:
        slug = q["slug"]
        if slug == "react-ignition":
            continue 
            
        q_dir = root / "data/quests" / slug
        workspace_dir = q_dir / "workspace"
        grading_dir = q_dir / "grading/public"
        
        # README
        readme_path = workspace_dir / "README.md"
        readme_content = get_file_content(readme_path)
        
        # Public Test
        test_files = list(grading_dir.glob("*.test.mjs"))
        public_test_path = test_files[0] if test_files else Path("MISSING_TEST")
        public_test_content = get_file_content(public_test_path) if test_files else "NO TEST FILE FOUND"
        
        # Workspace Starter
        task_path = workspace_dir / "task.mjs"
        if not task_path.exists():
             task_path = workspace_dir / "task.jsx"
        workspace_content = get_file_content(task_path)
        
        # Meta
        meta = {
            "slug": slug,
            "tier": 1,
            "world": "world-react",
            "readme_path": str(readme_path.as_posix()),
            "public_test_path": str(public_test_path.as_posix()),
            "workspace_paths": [str(task_path.as_posix())],
            "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
        }
        
        packet = f"""### Quest Packet: {slug}

**README.md**

```md
{readme_content}
```

**Public Test**

```javascript
{public_test_content}
```

**Workspace Starter**

```javascript
{workspace_content}
```

**Meta**

```json
{json.dumps(meta, indent=2)}
```
"""
        output.append(packet)
        count += 1
        
    final_output = "\n\n".join(output)
    final_output += f"\n\nReact quest packets complete: {count}/{len(quests)-1} sent."
    
    print(final_output)

if __name__ == "__main__":
    main()
