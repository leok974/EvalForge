from __future__ import annotations
import os
import time
import tempfile
import subprocess
from dataclasses import dataclass
from arcade_app.services.runner_registry import RunnerRegistry

@dataclass
class ExecResult:
    ok: bool
    exit_code: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool

from typing import Optional, Dict, Any

def run_code_docker(language: str, code: str, stdin: str = "", timeout_ms: int = 2500, workspace: Optional[Dict[str, Any]] = None, mode: str = "run") -> ExecResult:
    """
    Safer execution: docker container, no network, capped resources, non-root, read-only.
    Requires docker installed + daemon running.
    """
    # 1. Determine Entrypoint
    entrypoint = "main.py"
    if language == "typescript": entrypoint = "main.ts"
    
    if workspace:
        entrypoint = workspace.get("entrypoint", entrypoint)
    elif code:
        pass # Legacy single file, defaults apply
    
    spec = RunnerRegistry.get_runner(language, mode=mode, entrypoint=entrypoint)
    image = os.getenv(f"EXECUTION_DOCKER_IMAGE_{language.upper()}", spec.docker_image)
    
    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="evalforge-docker-run-") as td:
        
        # 2. Write Files
        if workspace:
            for f in workspace.get("files", []):
                path = f["path"]
                content = f["content"]
                # Prevent traversal
                if ".." in path or path.startswith("/"): continue
                
                full_path = os.path.join(td, path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as wf:
                    wf.write(content)

            # Inject Python Test Runner
            if mode == "tests" and language == "python":
                runner_dir = os.path.join(td, ".evalforge")
                os.makedirs(runner_dir, exist_ok=True)
                runner_target = os.path.join(runner_dir, "run_unittest_json.py")
                
                # Source path assumption: same specific directory
                src_path = os.path.join(os.path.dirname(__file__), "run_unittest_json.py")
                if os.path.exists(src_path):
                    with open(src_path, "r", encoding="utf-8") as rf:
                        with open(runner_target, "w", encoding="utf-8") as wf:
                            wf.write(rf.read())
        else:
            # Legacy Single File
            main_file = os.path.join(td, spec.file_name)
            with open(main_file, "w", encoding="utf-8") as f:
                f.write(code)

        # Windows path note: Docker Desktop can mount temp dirs; keep it simple.
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
            # Inject env vars from spec
            *sum([["-e", f"{k}={v}"] for k, v in spec.env.items()], []),
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "-e", "PYTHONIOENCODING=utf-8",
            image,
            *spec.command
        ]

        try:
            p = subprocess.run(
                cmd,
                input=stdin.encode("utf-8") if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=max(0.1, (timeout_ms + 1000) / 1000.0), # Add buffer for docker overhead
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
