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

def run_python_local(code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None) -> ExecResult:
    """
    DEV ONLY. Not safe for untrusted code. Use docker backend for prod.
    Runs python with:
      -I isolated mode, -B no bytecode
    """
    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="evalforge-run-") as td:
        # Write workspace files if present
        has_main = False
        if workspace and "files" in workspace:
             for f in workspace["files"]:
                 f_path = f.get("path")
                 f_content = f.get("content", "")
                 if f_path:
                     # Check if this is main.py (normalize path separation just in case)
                     if os.path.normpath(f_path) == "main.py":
                         has_main = True
                         
                     full_path = os.path.join(td, f_path)
                     # Ensure dirs exist
                     os.makedirs(os.path.dirname(full_path), exist_ok=True)
                     with open(full_path, "w", encoding="utf-8") as fw:
                         fw.write(f_content)
                         
        # Fallback/Primary: write 'code' to main.py ONLY if not already provided by workspace
        if code and not has_main:
            path = os.path.join(td, "main.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
        
        # Determine target file
        target_file = "main.py"
        if workspace and workspace.get("entrypoint"):
            target_file = workspace["entrypoint"]
        
        path = os.path.join(td, target_file)
        # If target file doesn't exist (e.g. wrong entrypoint or empty workspace), we might fail.
        # But we let subprocess handle the error or check here?
        # The original code had a check, let's keep basic sanity check or just run it.
        
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

def run_code(language: str, code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, mode: str = "run") -> ExecResult:
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
        return run_code_docker(language, code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, mode=mode)
        
    return run_python_local(code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace)

# Alias for backward compatibility if needed, but we should switch callers
run_python = lambda c, s="", t=2000: run_code("python", c, s, t)
