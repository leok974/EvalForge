from typing import List, Dict, Any
from arcade_app.services.security import safe_relpath, validate_workspace_limits

def build_effective_workspace(base_workspace: Dict[str, Any], overlay_files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministically merges overlay files into the base workspace.
    
    Rules:
    - Base workspace defines 'editable' flags.
    - Overlay can only modify files that are 'editable=True' in base.
    - Overlay cannot add new files (for now, stricter Phase 6.1 rule).
    - Entrypoint is immutable from base configuration.
    - Output is sorted by path.
    - Validates all paths and limits.
    """
    
    # 1. Normalize Base
    base_files = base_workspace.get("files", [])
    if isinstance(base_files, dict):
        base_files = [{"path": k, "content": v, "editable": True} for k, v in base_files.items()]
    entrypoint = base_workspace.get("entrypoint", "main.py")
    
    # Map path -> file_def
    effective_map = {}
    
    for bf in base_files:
        path = safe_relpath(bf["path"])
        effective_map[path] = {
            "path": path,
            "content": bf["content"],
            "editable": bf.get("editable", True) # Default to true for base, though legacy logic might differ? 
            # Actually default editable=True is reasonable for base definitions if unspecified.
        }

    # 2. Process Overlay
    # Validate limits on overlay first? Or on final result?
    # Let's validate overlay STRUCTURE first.
    if isinstance(overlay_files, dict):
        overlay_files = [{"path": k, "content": v} for k, v in overlay_files.items()]
    
    for of in overlay_files:
        path = safe_relpath(of["path"])
        content = of["content"]
        
        if path not in effective_map:
            # Reject new files for now
            # In future we might allow if size permits, but hardening plan says restrictive.
            # "Overlay cannot add new files unless explicitly allowed later"
            continue 
            
        base_def = effective_map[path]
        if not base_def["editable"]:
             # Skip or Error? Plan says "Overlay may only include files where base has editable=true"
             # Silent ignore is safer/more robust than 400 for stray edits
             continue
             
        # Apply Edit
        effective_map[path]["content"] = content

    # 3. Final Construction
    final_files = sorted(effective_map.values(), key=lambda x: x["path"])
    
    # 4. Global Limit Check
    validate_workspace_limits(final_files)
    
    return {
        "entrypoint": entrypoint,
        "files": final_files
    }

def inject_sql_task(workspace: Dict[str, Any], code: str) -> Dict[str, Any]:
    """
    Deterministically injects the student's SQL code as 'task.sql' into the workspace.
    Overrides any existing 'task.sql' or 'workspace/task.sql' to ensure the runner
    always executes the provided code.
    """
    if workspace is None:
        workspace = {}
        
    run_files = workspace.get("files", [])
    if isinstance(run_files, dict):
        run_files = [{"path": k, "content": v} for k, v in run_files.items()]
    
    # Remove existing task.sql (normalize paths aggressively for this specific check)
    filtered_files = []
    for f in run_files:
        p = f.get("path", "")
        # Prevent both raw 'task.sql' and nested 'workspace/task.sql' tricks
        if p == "task.sql" or p.endswith("/task.sql") or p.endswith("\\task.sql"):
            continue
        filtered_files.append(f)
        
    # Inject exactly "task.sql"
    filtered_files.append({
        "path": "task.sql",
        "content": code
    })
    
    workspace["files"] = filtered_files
    workspace["entrypoint"] = "task.sql"
    
    return workspace
