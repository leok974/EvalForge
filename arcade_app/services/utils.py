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
