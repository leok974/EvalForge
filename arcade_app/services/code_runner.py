from __future__ import annotations
import os
import sys
import time
import tempfile
import subprocess
from dataclasses import dataclass


@dataclass
class ExecResult:
    ok: bool
    exit_code: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool

def run_python_local(code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, quest_slug: Optional[str] = None) -> ExecResult:
    """
    DEV ONLY. Not safe for untrusted code. Use docker backend for prod.
    Runs python with:
      -I isolated mode, -B no bytecode
    """
    t0 = time.time()
    import logging
    logger = logging.getLogger("code_runner")

    with tempfile.TemporaryDirectory(prefix="evalforge-run-") as td:
        # Write workspace files if present
        files = workspace.get("files", []) if workspace else []

        # Fallback: If no files provided, try to load from disk using quest_slug
        if not files and quest_slug:
            # Need to find where data/quests is relative to CWD
            # app is usually at d:\EvalForge or /app in container
            # Try a few standard locations
            possible_roots = ["/app/data/quests", "d:\\EvalForge\\data\\quests", "./data/quests", "../data/quests"]
            quest_dir = None
            for r in possible_roots:
                p = os.path.join(r, quest_slug, "workspace")
                if os.path.exists(p):
                    quest_dir = p
                    break
            
            if quest_dir:
                logger.info(f"Fallback: Loading workspace from {quest_dir}")
                for root, _, filenames in os.walk(quest_dir):
                    for filename in filenames:
                        abs_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(abs_path, quest_dir)
                        # Skip hidden files/dirs
                        if any(p.startswith(".") for p in rel_path.split(os.sep)):
                            continue
                        try:
                            with open(abs_path, "r", encoding="utf-8") as f:
                                files.append({"path": rel_path, "content": f.read()})
                        except Exception:
                            pass 

        has_main = False
        
        # If still no files and we have 'code', use legacy mode
        if not files and code:
             # Legacy Single File
             path = os.path.join(td, "main.py")
             with open(path, "w", encoding="utf-8") as f:
                 f.write(code)
             has_main = True
        else:
             for f in files:
                 path = f["path"]
                 content = f["content"]
                 # Prevent traversal
                 if ".." in path or path.startswith("/"): continue
                 
                 # Path Normalization: Strip workspace/ prefix
                 if path.startswith("workspace/") or path.startswith("workspace\\"):
                     path = path[10:]
                 elif path.startswith("workspace") and (len(path) > 9 and path[9] in [os.sep, '/']):
                     path = path[10:]
                     
                 if os.path.normpath(path) == "main.py":
                     has_main = True

                 full_path = os.path.join(td, path)
                 os.makedirs(os.path.dirname(full_path), exist_ok=True)
                 with open(full_path, "w", encoding="utf-8") as fw:
                     fw.write(content)
                         
        # Determine target file
        target_file = "main.py"
        if workspace and workspace.get("entrypoint"):
            target_file = workspace["entrypoint"]
            # Normalize entrypoint too if it has workspace/
            if target_file.startswith("workspace/") or target_file.startswith("workspace\\"):
                target_file = target_file[10:]

        # Preflight Check & Entrypoint Resolution
        listing = []
        for root, _, filenames in os.walk(td):
            for f in filenames:
                listing.append(os.path.relpath(os.path.join(root, f), td))

        effective_entrypoint = "main.py"
        found_configured = False
        if workspace and workspace.get("entrypoint"):
             if workspace["entrypoint"] in listing:
                 effective_entrypoint = workspace["entrypoint"]
                 found_configured = True
                 
        if not found_configured:
            # Auto-detect for Python local runner
            if "task.py" in listing:
                effective_entrypoint = "task.py"
            elif "main.py" in listing:
                effective_entrypoint = "main.py"
        
        path = os.path.join(td, effective_entrypoint)
        if not os.path.exists(path):
            error_msg = f"SYSTEM_ERROR: WORKSPACE_MISSING: Entrypoint '{effective_entrypoint}' not found in workspace.\n"
            error_msg += f"Written files: {listing}\n"
            return ExecResult(
                ok=False,
                exit_code=2, 
                duration_ms=0,
                stdout="",
                stderr=error_msg,
                timed_out=False
             )
        
        # Using sys.executable is safer for local dev if venv is active.
        cmd = [sys.executable, "-B", path]

        env = {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": td # explicitly add cwd to path? python adds script dir by default.
        }

        try:
            p = subprocess.run(
                cmd,
                input=stdin.encode("utf-8") if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=td,
                env=env,
                timeout=max(0.1, timeout_ms / 1000.0),
            )
            
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=(p.returncode == 0),
                exit_code=p.returncode,
                duration_ms=dt,
                stdout=p.stdout.decode("utf-8", errors="replace"),
                stderr=p.stderr.decode("utf-8", errors="replace"),
                timed_out=False,
            )
        except subprocess.TimeoutExpired as e:
            dt = int((time.time() - t0) * 1000)
            out = (e.stdout or b"").decode("utf-8", errors="replace")
            err = (e.stderr or b"").decode("utf-8", errors="replace")
            return ExecResult(
                ok=False,
                exit_code=None,
                duration_ms=dt,
                stdout=out,
                stderr=err + ("\n[Timed out]" if err else "[Timed out]"),
                timed_out=True,
            )

from typing import Optional, Dict, Any

def run_code(language: str, code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, mode: str = "run", quest_slug: Optional[str] = None) -> ExecResult:
    """
    Dispatcher for code execution.
    - Python: Supports 'local' (dev) or 'docker'.
    - Other (TS): Requires 'docker'.
    """
    backend = os.getenv("EXECUTION_BACKEND", "local")
    
    # Force docker for non-python or if explicitly set.
    # Workspace support now added to local runner for Python.
    # CRITICAL: mode='tests' requires Docker because local runner cannot inject the test harness (run_unittest_json.py).
    use_docker = (backend == "docker") or (language != "python") or (mode == "tests")

    if use_docker:
        from arcade_app.services.code_runner_docker import run_code_docker
        return run_code_docker(language, code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, mode=mode, quest_slug=quest_slug)
        
    return run_python_local(code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, quest_slug=quest_slug)

# Alias for backward compatibility if needed, but we should switch callers
run_python = lambda c, s="", t=2000: run_code("python", c, s, t)
