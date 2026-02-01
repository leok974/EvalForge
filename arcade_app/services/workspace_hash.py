"""
Phase 8.x PR 4: Workspace Hash Helper

Provides deterministic canonical hashing for workspace snapshots.
Used for replay debugging, drift detection, and deduplication.
"""
import hashlib
from typing import Dict, List, Any, Optional


def hash_workspace_snapshot(workspace_snapshot: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Compute canonical hash of workspace snapshot.
    
    Deterministic hashing rules:
    1. Sort files by path (stable ordering)
    2. Include entrypoint if present
    3. Hash format: "sha256:<hexdigest>"
    
    Args:
        workspace_snapshot: Dict with optional "files" and "entrypoint" keys
        
    Returns:
        "sha256:<hex>" or None if workspace is empty/None
        
    Example:
        >>> ws = {
        ...     "entrypoint": "main.py",
        ...     "files": [
        ...         {"path": "utils.py", "content": "def helper(): pass"},
        ...         {"path": "main.py", "content": "from utils import helper"}
        ...     ]
        ... }
        >>> hash_workspace_snapshot(ws)
        'sha256:abc123...'
    """
    if not workspace_snapshot:
        return None
    
    files = workspace_snapshot.get("files") or []
    if not files:
        return None
    
    entrypoint = workspace_snapshot.get("entrypoint") or ""
    
    # Build canonical representation
    parts = [f"entrypoint:{entrypoint}"]
    
    # Sort files by path for deterministic ordering
    sorted_files = sorted(files, key=lambda f: f.get("path", ""))
    
    for file in sorted_files:
        path = file.get("path", "")
        content = file.get("content", "")
        parts.append(path)
        parts.append(content)
    
    # Hash the canonical representation
    payload = "\n".join(parts).encode("utf-8")
    hex_digest = hashlib.sha256(payload).hexdigest()
    
    return f"sha256:{hex_digest}"


def build_execution_context(
    language: str,
    mode: str,
    duration_ms: int,
    exit_code: int,
    stdout: Optional[str],
    stderr: Optional[str],
    timed_out: bool,
    runner_backend: str = "docker"
) -> Dict[str, Any]:
    """
    Build safe execution context metadata.
    
    SAFETY: Does NOT include:
    - Absolute paths
    - Environment variables
    - Tokens/secrets
    - Raw hidden test output
    
    Args:
        language: Programming language (e.g. "python", "typescript")
        mode: Execution mode (e.g. "validate", "execute", "tests")
        duration_ms: Execution duration in milliseconds
        exit_code: Process exit code
        stdout: Standard output (for size calculation only)
        stderr: Standard error (for size calculation only)
        timed_out: Whether execution timed out
        runner_backend: Execution backend (default: "docker")
        
    Returns:
        Safe metadata dict suitable for JSONB storage
    """
    return {
        "runner_backend": runner_backend,
        "mode": mode,
        "language": language,
        "duration_ms": duration_ms,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "stdout_bytes": len(stdout or ""),
        "stderr_bytes": len(stderr or ""),
        # Optional: add image/version info if available
        # "image": "python:3.11-slim",  # Example
    }
