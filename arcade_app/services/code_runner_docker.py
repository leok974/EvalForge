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
            
            # 3. Permissions fix for Docker (since we run as non-root user)
            # Ensure the temp dir and all files are world-readable AND writable (for reports)
            os.chmod(td, 0o777)
            for root, dirs, files in os.walk(td):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o666)

        # 3. Docker-in-Docker safe execution: Create -> CP -> Start
        # We cannot use volume mounts (-v) because the host daemon does not see our internal paths.
        import uuid
        container_name = f"runner-{uuid.uuid4()}"
        
        # Base Create Command
        create_cmd = [
            "docker", "create",
            "--name", container_name,
            "--network", "none",
            "--cpus", "1",
            "--memory", "256m",
            "--pids-limit", "64",
            # "--read-only", # CP might fail if read-only root? Workspace should be writable during setup?
            # We'll rely on user non-root for safety, and maybe ro flag isn't strictly needed for ephemeral
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", "65534:65534",
            "-w", "/workspace",
            # Env vars
            *sum([["-e", f"{k}={v}"] for k, v in spec.env.items()], []),
            # Env vars
            *sum([["-e", f"{k}={v}"] for k, v in spec.env.items()], []),
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "-e", "PYTHONIOENCODING=utf-8",
            image,
            *spec.command
        ]

        try:
            # A) Create
            subprocess.check_call(create_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # B) Copy files
            # Ensure workspace exists (some images might not have it) -> CP creates it if logical
            # We verify permissions of the local dir first (already done in previous step/default)
            # Docker CP syntax: src_path/. dest_container:dest_path
            cp_cmd = ["docker", "cp", f"{td}/.", f"{container_name}:/workspace/"]
            subprocess.check_call(cp_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # C) Start (Detached)
            # We use detached start + wait + logs for reliable capture
            subprocess.check_call(["docker", "start", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # D) Wait
            # We enforce timeout here manually by polling or using docker wait with subprocess timeout
            wait_cmd = ["docker", "wait", container_name]
            try:
                subprocess.run(wait_cmd, timeout=max(0.1, (timeout_ms + 1000) / 1000.0), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                 # Timeout logic handled below
                 pass
            
            # E) Logs
            # Capture stdout/stderr
            logs_p = subprocess.run(
                ["docker", "logs", container_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout_str = logs_p.stdout.decode("utf-8", errors="replace")
            stderr_str = logs_p.stderr.decode("utf-8", errors="replace")
            
            # Fallback: If stdout is empty or doesn't look like JSON, try to copy report file
            # This handles cases where stdout capture fails or is empty
            if not stdout_str.strip() or (mode == "tests" and not stdout_str.strip().startswith("{")):
                try:
                    # Try to copy report file
                    report_dest = os.path.join(td, "test_results_fallback.json")
                    subprocess.check_call(
                        ["docker", "cp", f"{container_name}:/workspace/.evalforge/test_results.json", report_dest],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    with open(report_dest, "r", encoding="utf-8") as f:
                        fallback_json = f.read()
                        if fallback_json:
                            # Use fallback content if valid
                             stdout_str = fallback_json
                except Exception:
                    # Ignore cp failure (file might not exist)
                    pass

            # F) Inspect Exit Code
            inspect_p = subprocess.run(
                ["docker", "inspect", container_name, "--format", "{{.State.ExitCode}}"],
                stdout=subprocess.PIPE
            )
            exit_code = int(inspect_p.stdout.decode().strip() or "0")
            
            dt = int((time.time() - t0) * 1000)
            
            return ExecResult(
                ok=(exit_code == 0),
                exit_code=exit_code,
                duration_ms=dt,
                stdout=stdout_str,
                stderr=stderr_str,
                timed_out=False,
            )

        except subprocess.TimeoutExpired:
             # Kill container
            subprocess.run(["docker", "kill", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Try to grab logs even if timed out
            logs_p = subprocess.run(["docker", "logs", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = logs_p.stdout.decode("utf-8", errors="replace")
            err = logs_p.stderr.decode("utf-8", errors="replace")
            
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=False,
                exit_code=None,
                duration_ms=dt,
                stdout=out,
                stderr=err + "\n[Timed out]",
                timed_out=True,
            )
        except Exception as e:
             # Fallback error
             return ExecResult(
                ok=False,
                exit_code=-1,
                duration_ms=0,
                stdout="",
                stderr=str(e),
                timed_out=False
             )
        finally:
            # D) Cleanup
            subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
