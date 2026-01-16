from __future__ import annotations
import os
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

def run_python_docker(code: str, stdin: str = "", timeout_ms: int = 2500) -> ExecResult:
    """
    Safer execution: docker container, no network, capped resources, non-root, read-only.
    Requires docker installed + daemon running.
    """
    image = os.getenv("EXECUTION_DOCKER_IMAGE", "python:3.12-slim")
    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="evalforge-docker-run-") as td:
        main_py = os.path.join(td, "main.py")
        with open(main_py, "w", encoding="utf-8") as f:
            f.write(code)

        # Windows path note: Docker Desktop can mount temp dirs; keep it simple.
        # If you ever hit mount issues on Windows, move temp under repo like ./tmp_runs.
        # Docker on Windows requires absolute paths for mounting
        mount_arg = f"{td}:/workspace:ro"

        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--cpus", "1",
            "--memory", "256m",
            "--pids-limit", "64",
            "--read-only",
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", "65534:65534",
            "-v", mount_arg,
            "-w", "/workspace",
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "-e", "PYTHONIOENCODING=utf-8",
            image,
            "python", "-I", "-B", "/workspace/main.py",
        ]

        try:
            p = subprocess.run(
                cmd,
                input=stdin.encode("utf-8") if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
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
