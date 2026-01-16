from __future__ import annotations
import os
import sys
import time
import tempfile
import subprocess
from dataclasses import dataclass
from arcade_app.services.code_runner_docker import run_python_docker

@dataclass
class ExecResult:
    ok: bool
    exit_code: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool

def run_python_local(code: str, stdin: str = "", timeout_ms: int = 2000) -> ExecResult:
    """
    DEV ONLY. Not safe for untrusted code. Use docker backend for prod.
    Runs python with:
      -I isolated mode, -B no bytecode
    """
    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="evalforge-run-") as td:
        path = os.path.join(td, "main.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        # Use current sys.executable to ensure we use the same python environment/version
        # if possible, or just "python" if we want generic. 
        # Using sys.executable is safer for local dev if venv is active.
        cmd = [sys.executable, "-I", "-B", path]

        env = {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            # keep env minimal, but inherit PATH maybe?
            # Ideally minimal to prevent leaking secrets
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

def run_python(code: str, stdin: str = "", timeout_ms: int = 2000) -> ExecResult:
    backend = os.getenv("EXECUTION_BACKEND", "local")
    if backend == "docker":
        return run_python_docker(code, stdin=stdin, timeout_ms=timeout_ms)
    return run_python_local(code, stdin=stdin, timeout_ms=timeout_ms)
